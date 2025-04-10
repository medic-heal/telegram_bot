from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

from decouple import config

item_ege = ['Базовая математика', 'Профильная математика', 'Физика', 'Химия', 'История', 'Обществознание', 'Информатика', 'Биология', 'География', 'Английский язык', 'Немецкий язык', 'Французский язык', 'Испанский язык', 'Китайский язык', 'Русский язык', 'Литература']

router = Router()

class Register(StatesGroup):
    name = State() 
    surname = State()

class EnterScore(StatesGroup):
    score = State()
    item_name = State()

def contains_digit(s):
    return any(char.isdigit() for char in s)

def validate_full_name(name):
    try:
        parts = name.split()
        if len(parts) != 2:
            raise ValueError("ФИО должно содержать ровно два слова, разделенных пробелом")
        first, last = parts
        if not (first.istitle() and last.istitle()):
            raise ValueError("Имя и фамилия должны начинаться с заглавной буквы")
        if not (first.isalpha() and last.isalpha()):
            raise ValueError("Имя и фамилия должны содержать только буквы")
        return True
    except ValueError as e:
        print(f"Ошибка: {e}")
        return False

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Привет! Выберите действие:\n\n /register - регистрация\n/enter_scores - ввод баллов ЕГЭ\n/view_scores - просмотреть введёные баллы ЕГЭ',
                         reply_markup=kb.main)


@router.message(Command('register'))
async def register(message: Message, state: FSMContext):

    get_register = await rq.get_user_register(message.from_user.id)
    if get_register:
        await message.answer("Вы уже зарегистрированы.", reply_markup=kb.main)
        return
    else:
        await state.set_state(Register.name)
        await message.answer('Введите имя и фамилию через пробел\n\nПример:\nМария Иванова')

@router.message(Register.name)
async def register_data(message: Message, state: FSMContext):
    try:
        message.text.split(' ')
    except:
        await message.answer('Информация введена неверно', reply_markup=kb.main)
        # await state.clear()
        return  
    else:
        if validate_full_name(message.text):
            await state.update_data(name=message.text.split(' ')[0])
            await state.update_data(surname=message.text.split(' ')[1])
            data = await state.get_data()
            await rq.set_name(message.from_user.id, data["name"], data["surname"])
            await message.answer('Регистрация прошла успешно', reply_markup=kb.main)
            await state.clear()
        else:
            await message.answer('Информация введена неверно', reply_markup=kb.main)
            # await state.clear()
    

@router.message(Command('enter_scores'))
async def enter_scores(message: Message, state: FSMContext):

    is_registered = await rq.is_user_registered(message.from_user.id)
    if not is_registered:
        await message.answer("Вы не зарегистрированы. Сначала введите имя и фамилию.", reply_markup=kb.main)
        return

    get_scores = await rq.get_user_scores(message.from_user.id)
    if get_scores:
        await message.answer("Вы уже ввели результаты экзаменов.", reply_markup=kb.main)
        return
    
    await state.set_state(EnterScore.item_name)
    await message.answer('Введите название предмета и балл:\n\nПример:\n\nРусский язык: 90\nПрофильная математика: 100')


@router.message(EnterScore.item_name)
async def enter_score_data(message: Message, state: FSMContext):
    try:
        message_from_user = message.text.split('\n')
        scores = []  
    except:
        await message.answer('Информация введена неверно', reply_markup=kb.main)
        await rq.delete_user_scores(message.from_user.id)
        # await state.clear()
        return  
    else:
        for i in range(len(message_from_user)):
            parts = message_from_user[i].split(': ')
            if len(parts) == 2 and parts[0] in item_ege and parts[1].isdigit():
                score = int(parts[1])
                if 0 <= score <= 100:
                    scores.append((parts[0], score))
                else:
                    await message.answer('Баллы должны быть в диапазоне 0-100', reply_markup=kb.main)
                    await rq.delete_user_scores(message.from_user.id)
                    await state.clear()
                    return
            else:
                await message.answer('Информация введена неверно', reply_markup=kb.main)
                await rq.delete_user_scores(message.from_user.id)
                # await state.clear()
                return  
        if len(scores) == len(set(scores)):
            for item_name, score in scores:
                await rq.set_score(message.from_user.id, item_name, score)
        else:
                await message.answer('Информация введена неверно', reply_markup=kb.main)
                await rq.delete_user_scores(message.from_user.id)
                # await state.clear()
                return          
    await message.answer('Баллы успешно внесены', reply_markup=kb.main)
    await state.clear()

@router.message(Command('view_scores'))
async def view_scores(message: Message):
    message_with_scores = await rq.get_user_scores(message.from_user.id)
    if not message_with_scores:
        await message.answer("Ваши результаты экзаменов ещё не введены.", reply_markup=kb.main)
        return
    
    message_for_send = '\n'.join(f"{item_name}: {score}" for item_name, score in message_with_scores)
    await message.answer(message_for_send)

@router.message(Command('clear_all_database'))
async def clear_database(message: Message):
    if message.from_user.id == int(config('ADMIN')):
        await rq.clear_database()
        await message.answer("База данных полностью очищена")
    else:
        await message.answer("У вас недостаточно прав")

@router.message(Command('view_all_database'))
async def view_database(message: Message):
    if message.from_user.id == int(config('ADMIN')):
        message_with_scores = await rq.get_all_students_scores()
        if not message_with_scores:
            await message.answer("Информация об учениках отсутствует", reply_markup=kb.main)
            return
        result = ""
        people = {}

        for first_name, last_name, subject, grade in message_with_scores:

            name_key = (first_name, last_name)
            if name_key not in people:
                people[name_key] = []

            if subject != None and grade != None:
                people[name_key].append((subject, grade))
            else:
                people[name_key].append(('Ввод данных', 'ожидается'))


        for (first_name, last_name), subjects in people.items():
            result += f"{first_name} {last_name}:\n"
            for subject, grade in subjects:
                result += f"{subject}: {grade}\n"
            result += "\n" 

        await message.answer(result)

    else:
        await message.answer("У вас недостаточно прав")