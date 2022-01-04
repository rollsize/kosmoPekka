from aiogram.utils.markdown import text, bold, italic, code
info = text("\"" + italic("KosmoPekka") + "\" – это текстовый квест в котором тебе предстоит побывать в космосе, разгадывать головоломки и сражаться с инопришиленцами. И лишь от",
bold("твоего"), "выбора зависит концовка игры.\n")
first_message = text("Здравствуй,",bold("дорогой друг") + "! Мы приветствуем тебя в нашей игре!\n" + info + code("Игра находиться в стадии разработки, поэтому сейчас доступен лишь пролог"))
commands = "/start, /help\n/rm - Убрать основную клавиатуру\n/rkm - Вернуть основную клавиатуру\n/delay число(0-8) - Изменить задержку появления текста"
contact_us = "Доступные команды:\n" + commands + "\n\nЕсли у вас возникли проблемы, напишите @"
use_help = "Я не знаю что с этим делать, используйте /help"
rkm = "Нарисовал кнопки, чтоб было удобнее. Удалить - /rm"
rm = "Убираю главное меню. Вернуть - /rkm"

plot = {
    "Prologue": {
        "Paragraph_1": {
            1: {"Text": ("Утром,1967 года 28-летний Коля Степанченко ехал на заднем сиденье “Волги”. Он направлялся из Киева на космодром “Сиреневый-1“, " +
                "на встречу со своим коллегой Игорем Шеховцовым. Машина, поднимая пыль проселочных дорог, оставляла позади небольшие дачные поселки и промышленные городки, " +
                "приближая ответственного за техническое оснащение “Рассвета” к новому месту работы")},
            2: {"Text": ("Всего через полтора часа в пути “Волга” миновала большой дорожный указатель “Юпитер” - так назывался город, в котором с 1960-х годов жили и тренировались " +
                "космонавты. Для каждого советского космонавта путь в космос начинался с этой дороги, Юрий Алексеевич тоже был не исключением. Главная дорога проходила мимо жилого " +
                "комплекса, где жили космонавты, обслуживающий персонал и члены их семей и вела к аэропорту - отсюда космонавтов отправляли на “Сиреневый-1”.")},
            3: {"Text": ("Пройдя второй КПП, Степанченко направился к Жилому-2 - небольшому зданию, в котором размещались спальни для двух человек. Здесь его ждал крепкий, рослый и умный, " +
                "других здесь и не могло быть, мужчина - Шеховцов.\n–Здравствуй, Николай, рад тебя приветствовать на базе космодрома “Сиреневый-1” - Шеховцов с легкой" +
                " улыбкой поприветствовал меня, протянув руку\n–Здравствуйте, я тоже рад знакомству. - Ответил я мужчине на вид лет сорока, пожав здоровую руку." +
                "\n– Раз уж ты здесь новенький, я покажу тебе что здесь и как, чтоб быстрее освоился.\n– Да, я бы не отказался, а то здесь я знаю только Вас." +
                " - Проговорил я, немного улыбнувшись.\n–Тогда, с чего начнём? - Спросил Шеховцев"),
                "Buttons": [["Командный пункт", 1], ["Жилой блок", 2], ["Технический комплекс", 3]] }
        },
        "Paragraph_2": {
            1: {}
        }
    }
}