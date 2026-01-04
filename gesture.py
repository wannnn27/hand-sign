import cv2
import mediapipe as mp
from gtts import gTTS
import pygame
import threading
import time
import os

# ==================== Voice Cache & Audio Setup ====================
VOICE_DIR = "voices"
if not os.path.exists(VOICE_DIR):
    os.makedirs(VOICE_DIR)

# Inisialisasi mixer pygame
pygame.mixer.init()

def play_voice(text):
    file_path = os.path.join(VOICE_DIR, text.replace(" ", "_") + ".mp3")

    # Jika MP3 belum ada, generate dan simpan cache
    if not os.path.isfile(file_path):
        tts = gTTS(text=text, lang="id")
        tts.save(file_path)

    # Play sound menggunakan pygame (non-blocking logic di thread terpisah)
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print(f"Error playing sound: {e}")

def speak_async(text):
    # Pastikan thread sebelumnya tidak tumpang tindih jika perlu, 
    # atau biarkan pygame queue handle (tapi music.load akan stop current).
    # Threading tetap digunakan agar main loop tidak freeze saat loading file.
    threading.Thread(target=play_voice, args=(text,), daemon=True).start()


# ==================== Gesture Setup ====================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

if not cap.isOpened():
    print("Error: Kamera tidak dapat diakses!")
    exit()

# Gesture Messages sesuai request
gesture_messages = {
    "FIVE": "Halo!",
    "TWO": "Perkenalkan",
    "ONE": "Saya Adi Arwan Syah",
    "ROCK": "Dari prodi Sistem Informasi",
    "THUMB": "Terima kasih"
}

last_gesture = None
last_time = 0
cooldown = 2.0  # detik (sedikit diperlama agar audio selesai)


# ==================== Gesture Detection ====================
def detect_gesture(hand, handType):
    lm = hand.landmark
    finger_tips = [8, 12, 16, 20]  # index, middle, ring, pinky

    fingers = []
    for tip in finger_tips:
        fingers.append(lm[tip].y < lm[tip - 2].y)

    thumb_tip = lm[4]
    thumb_base = lm[2]

    # Detect jempol berbeda untuk Left / Right hand
    if handType == "Right":
        thumb_open = thumb_tip.x < thumb_base.x
    else:
        thumb_open = thumb_tip.x > thumb_base.x

    # Mapping gestures - LOGIC DIPERBAIKI AGAR LEBIH AKURAT
    # FIVE: Semua jari terbuka
    if all(fingers) and thumb_open:
        return "FIVE"
    
    # TWO: Telunjuk & Tengah terbuka, lainnya tertutup
    if fingers == [True, True, False, False] and not thumb_open:
        return "TWO"
    
    # ONE: Hanya Telunjuk terbuka
    if fingers == [True, False, False, False] and not thumb_open:
        return "ONE"
    
    # ROCK: Telunjuk & Kelingking terbuka? Atau Jempol & Kelingking?
    # Biasanya rock n roll = Index(8) & Pinky(20). 
    # Tapi kode lama: [False, False, False, True] + Thumb open => Jempol & Kelingking
    if fingers == [False, False, False, True] and thumb_open:
        return "ROCK"
        
    # THUMB: Hanya jempol, jari lain kepal
    if not any(fingers) and thumb_open:
        return "THUMB"

    return None


# ==================== Main Loop ====================
print("Program berjalan... Tekan ESC untuk keluar.")
while True:
    success, frame = cap.read()
    if not success:
        print("Gagal membaca frame kamera.")
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture = None
    if result.multi_hand_landmarks:
        for idx, hand in enumerate(result.multi_hand_landmarks):
            # Cek handedness label
            if result.multi_handedness:
                handType = result.multi_handedness[idx].classification[0].label
            else:
                handType = "Right" # Default fallback
                
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            gesture = detect_gesture(hand, handType)

    if gesture and gesture in gesture_messages:
        text = gesture_messages[gesture]

        cv2.putText(frame, text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 3)

        # Cegah suara berulang-ulang cepat
        if gesture != last_gesture and (time.time() - last_time) > cooldown:
            speak_async(text)
            last_gesture = gesture
            last_time = time.time()
    else:
        # Reset last_gesture jika tangan hilang/berubah, opsional
        # last_gesture = None 
        pass

    cv2.imshow("Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC kelua
        break

cap.release()
cv2.destroyAllWindows()
