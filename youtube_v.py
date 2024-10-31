import yt_dlp
import ffmpeg
import os

def download_and_trim_audio(url, start_time, output_name):
    # Скачивание аудио с помощью yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloaded_audio.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_path = ydl.prepare_filename(info_dict)
    
    # Конвертация формата времени в секунды для ffmpeg
    def convert_timecode(timecode):
        minutes, seconds = map(int, timecode.split(":"))
        return minutes * 60 + seconds

    start_seconds = convert_timecode(start_time)
    end_seconds = start_seconds + 25  # Всегда 15 секунд от начала

    # Обрезка и конвертация в mp3 с помощью ffmpeg
    trimmed_audio_path = f"{output_name}.mp3"
    (
        ffmpeg
        .input(audio_path, ss=start_seconds, to=end_seconds)
        .output(trimmed_audio_path, format="mp3", acodec="libmp3lame")
        .run(overwrite_output=True)
    )
    
    # Удаление исходного файла
    os.remove(audio_path)
    print(f"Аудио сохранено как {trimmed_audio_path}")

if __name__ == "__main__":
    # Запрос данных у пользователя
    url = input("Введите ссылку на видео YouTube: ")
    start_time = input("Введите начальный тайм-код (в формате ММ:СС): ")

    # Предлагаем выбор имени файла
    words = ["TikTok", "Eurovision", "2k17", "Minus"]
    numbers = ["100", "200", "300", "400", "500"]

    print("Выберите слово для имени файла:")
    for i, word in enumerate(words, 1):
        print(f"{i}. {word}")
    word_choice = int(input("Введите номер слова: ")) - 1

    print("Выберите номер для имени файла:")
    for i, number in enumerate(numbers, 1):
        print(f"{i}. {number}")
    number_choice = int(input("Введите номер: ")) - 1

    # Формируем название файла
    output_name = f"{words[word_choice]}_{numbers[number_choice]}"
    
    # Запускаем загрузку и обрезку аудио
    download_and_trim_audio(url, start_time, output_name)
