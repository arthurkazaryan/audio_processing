import noisereduce as nr
import sys
from pyannote.audio import Pipeline
from scipy.io import wavfile
from pathlib import Path
from settings import paths_data


def diarization(path_to_file: Path, sample_rate, pause_length):

    pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization')
    diarizat = pipeline(path_to_file)
    speakers = {}

    for turn, _, speaker in diarizat.itertracks(yield_label=True):
        if speaker not in speakers:
            speakers[speaker] = []
        speakers[speaker].append([turn.start, turn.end])

    for speaker, data in speakers.items():
        real_fragments = []
        cur_range = []
        for i in range(len(data)-1):
            if not cur_range:
                cur_range.append(int(data[i][0] * sample_rate))
            second_target = data[i][1]
            if data[i+1][0] - second_target < pause_length:
                continue
            else:
                cur_range.append(int(second_target * sample_rate))
                real_fragments.append(cur_range)
                cur_range = []
        if cur_range:
            cur_range.append(int(data[-1][1] * sample_rate))
            real_fragments.append(cur_range)
        speakers[speaker] = real_fragments

    return speakers


if __name__ == '__main__':
    for path in sys.argv[2:]:
        file_path = Path(path)
        # Открываем аудиофайл
        sr, audio = wavfile.read(file_path)
        # Выясняем количество спикеров и когда они разговаривают
        speakers = diarization(file_path, sr, float(sys.argv[1]))
        # Делим аудио на спикеров и добавляем в отдельную аудиодорожку
        for speaker, cuts in speakers.items():
            # audio_output = np.zeros_like(audio)
            for idx, cut in enumerate(cuts):
                if len(audio.shape) > 1:
                    for i in range(len(audio.shape)):
                        audio_to_save = nr.reduce_noise(audio[:, i][cut[0]: cut[1]], sr=sr)
                else:
                    audio_to_save = nr.reduce_noise(audio[cut[0]: cut[1]], sr=sr)
                wavfile.write(paths_data.processed_folder.joinpath(f"{file_path.stem}_{speaker}_{idx + 1}.wav"),
                              sr, audio_to_save)
