import { Pizza, ExtraItem, Category } from '../types/pizza';

export const PIZZAS: Pizza[] = [
  {
    id: 1,
    name: 'Пепперони',
    description: 'Американская классика с пикантной колбаской пепперони, нежной моцареллой и фирменным томатным соусом.',
    ingredients: [
      'Пикантная пепперони',
      'Сыр моцарелла',
      'Фирменный томатный соус',
      'Орегано и итальянские травы'
    ],
    category: 'pizzas',
    image: 'https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&w=800&q=80',
    prices: {
      25: 45000,
      30: 60000,
      35: 75000,
    },
    calories: 275,
    weight: {
      25: '410 г',
      30: '590 г',
      35: '780 г',
    },
    isPopular: true,
    badge: '🔥 Хит продаж'
  },
  {
    id: 2,
    name: 'Маргарита',
    description: 'Истинная итальянская классика со свежими томатами, ароматным базиликом и отборной моцареллой.',
    ingredients: [
      'Сыр моцарелла рассольная',
      'Свежие спелые томаты',
      'Фирменный томатный соус Mutti',
      'Свежий зеленый базилик',
      'Оливковое масло первого отжима'
    ],
    category: 'pizzas',
    image: 'https://images.unsplash.com/photo-1604382355076-af4b0eb60143?auto=format&fit=crop&w=800&q=80',
    prices: {
      25: 40000,
      30: 52000,
      35: 65000,
    },
    calories: 230,
    weight: {
      25: '380 г',
      30: '540 г',
      35: '710 г',
    },
    badge: '🌿 Вегетарианская'
  },
  {
    id: 3,
    name: '4 сыра',
    description: 'Изысканное сочетание четырех благородных сыров на сливочной подушке для истинных гурманов.',
    ingredients: [
      'Сыр моцарелла',
      'Сыр дор блю с голубой плесенью',
      'Ароматный пармезан',
      'Классический чеддер',
      'Нежный сливочный соус альфредо'
    ],
    category: 'pizzas',
    image: 'https://images.unsplash.com/photo-1573821663912-569905455b1a?auto=format&fit=crop&w=800&q=80',
    prices: {
      25: 48000,
      30: 64000,
      35: 80000,
    },
    calories: 290,
    weight: {
      25: '400 г',
      30: '580 г',
      35: '760 г',
    },
    isPopular: true,
    badge: '🧀 Сырный рай'
  },
  {
    id: 4,
    name: 'Гавайская',
    description: 'Нежное запеченное куриное филе, сочные тропические ананасы и тягучая моцарелла под томатным соусом.',
    ingredients: [
      'Филе цыпленка су-вид',
      'Сладкие кусочки ананаса',
      'Сыр моцарелла',
      'Томатный соус PizzaHouse',
      'Прованские травы'
    ],
    category: 'pizzas',
    image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=800&q=80',
    prices: {
      25: 45000,
      30: 58000,
      35: 72000,
    },
    calories: 245,
    weight: {
      25: '420 г',
      30: '610 г',
      35: '800 г',
    },
    badge: '🍍 Экзотика'
  },
  {
    id: 5,
    name: 'BBQ Chicken',
    description: 'Ароматная курочка на гриле, хрустящий копченый бекон, красный крымский лук и дымный соус BBQ.',
    ingredients: [
      'Копченое куриное филе',
      'Хрустящий бекон',
      'Красный салатный лук',
      'Сыр моцарелла',
      'Крафтовый соус BBQ'
    ],
    category: 'pizzas',
    image: 'https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?auto=format&fit=crop&w=800&q=80',
    prices: {
      25: 48000,
      30: 65000,
      35: 82000,
    },
    calories: 285,
    weight: {
      25: '430 г',
      30: '620 г',
      35: '820 г',
    },
    isPopular: true,
    badge: '🍗 BBQ гриль'
  },
  {
    id: 6,
    name: 'Мясная',
    description: 'Максимум отборного мяса: острая пепперони, нежная ветчина, говяжий фарш и охотничьи колбаски.',
    ingredients: [
      'Пепперони',
      'Ветчина из индейки',
      'Пряный говяжий фарш',
      'Баварские охотничьи колбаски',
      'Сыр моцарелла',
      'Томатный соус'
    ],
    category: 'pizzas',
    image: 'https://images.unsplash.com/photo-1534308983496-4fabb1a015ee?auto=format&fit=crop&w=800&q=80',
    prices: {
      25: 52000,
      30: 70000,
      35: 88000,
    },
    calories: 315,
    weight: {
      25: '450 г',
      30: '650 г',
      35: '860 г',
    },
    isPopular: true,
    badge: '🥩 Мясной гигант'
  }
];

export const EXTRA_ITEMS: ExtraItem[] = [
  {
    id: 'combo-1',
    name: 'Комбо «Друзья»',
    description: '2 пиццы 30 см (Пепперони + 4 Сыра) и 2 напитка Coca-Cola 0.5 л со скидкой 20%',
    category: 'combos',
    image: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80',
    price: 110000,
    badge: '-20%'
  },
  {
    id: 'combo-2',
    name: 'Комбо «Мясной пир»',
    description: 'Пицца Мясная 35 см + Картофель фри с сырным соусом + Напиток 1 л',
    category: 'combos',
    image: 'https://images.unsplash.com/photo-1544982503-9f984c14501a?auto=format&fit=crop&w=800&q=80',
    price: 99000,
    badge: 'Выгодно'
  },
  {
    id: 'drink-1',
    name: 'Coca-Cola 0.5л',
    description: 'Освежающий классический газированный напиток в стеклянной бутылке',
    category: 'drinks',
    image: 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=800&q=80',
    price: 12000
  },
  {
    id: 'drink-2',
    name: 'Домашний лимонад маракуйя 0.4л',
    description: 'Освежающий авторский лимонад с натуральным пюре маракуйи и мятой',
    category: 'drinks',
    image: 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=800&q=80',
    price: 18000,
    badge: 'Холодный'
  },
  {
    id: 'dessert-1',
    name: 'Чизкейк Нью-Йорк',
    description: 'Классический нежный сливочный чизкейк с ягодным соусом',
    category: 'desserts',
    image: 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=800&q=80',
    price: 25000
  },
  {
    id: 'dessert-2',
    name: 'Шоколадный Брауни',
    description: 'Теплый шоколадный десерт с тающей сердцевиной из бельгийского шоколада',
    category: 'desserts',
    image: 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=800&q=80',
    price: 24000
  }
];

export const CATEGORIES: Category[] = [
  { id: 'pizzas', name: 'Пиццы', icon: 'Pizza', emoji: '🍕' },
  { id: 'combos', name: 'Комбо', icon: 'Package', emoji: '🍔' },
  { id: 'drinks', name: 'Напитки', icon: 'CupSoda', emoji: '🥤' },
  { id: 'desserts', name: 'Десерты', icon: 'Cake', emoji: '🍰' },
];

export const DEFAULT_BOT_USERNAME = 'absurddddbot';
