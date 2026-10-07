# Yafho-Silicare — кредиты и лицензии

## Музыка
| Файл в `assets/music/` | Трек / автор | Источник | Лицензия | Где используется |
|---|---|---|---|---|
| `yafho_ambient_v2.wav` | «Yafho ambient v2» — собственная музыка, синтезирована кодом (`projects/yafho/make_music.py`) | создано в проекте | без ограничений: сторонних сэмплов и лицензий нет | hero v2 9:16, 16:9, 4:5 и нарезки |

Требования: спокойный эмбиент 80–95 BPM, громкость в ролике 0.08–0.12 (по умолчанию 0.10).
Чтобы заменить трек на сторонний (Pixabay Music / YouTube Audio Library), положите файл в `assets/music/`, удалите `yafho_ambient_v2.wav` и заполните строку выше. Пересоздать собственный трек: `python projects/yafho/make_music.py`.

## Видео (Kling)
Клипы H01, H04–H08 генерируются вручную в Kling по промптам из `TZ.md`, раздел 2.

## Шрифты
Onest, JetBrains Mono — SIL Open Font License 1.1 (Google Fonts).
