class Pagination{

	items = [] // преобразованный набор данных
	catalog_items // изначальный набор данных
	count_items_page // количество объектов на странице
	total_page // количество страниц

	prev_btn = document.querySelector('div.pagination div.prev')
	next_btn = document.querySelector('div.pagination div.next')
	page_num = document.querySelector('div.pagination span.page-num')

	index = 1 // индекс страницы

	constructor(catalog_items, count_items_page){
		this.catalog_items = catalog_items
		this.count_items_page = count_items_page
		this.total_page = Math.ceil(catalog_items.length / count_items_page) // округляем в большую сторону
	}

	init(){
		this.page_num.textContent = this.index // установка в счетчик значения индекса


		var hold_arr = [] // вспомогательная переменная
		for (const item of this.catalog_items) {

			hold_arr.push(item) // вкладываем объекты в вспомогательный массив

			if(hold_arr.length == this.count_items_page){ // пока размер массива не будет равен количеству объектов на странице
				this.items.push(hold_arr) // вкладываем массив в переменную с преобразованными данными
				hold_arr = [] // очищаем вспомогательный массив
			}
		}

		if(hold_arr.length > 0){ // если вспомогательный массив не пуст
			this.items.push(hold_arr) // добавляем в преобразованный данные
		}

		// события кнопок
		// кнопка назад
		this.prev_btn.onclick = () => {
			if(this.index > 1){ // если индекс страницы больше 1
				this.index -= 1 // уменьшаем индекс
			}

			if(this.index === 1){ // если индекс равен 1
				this.disablePrev() // отключаем кнопку назад
				this.activeNext() // включаем кнопку вперед
			}

			this.page_num.textContent = this.index

			this.showByIndex() // отображаем по индексу
		}

		// кнопка вперед
		this.next_btn.onclick = () => {
			if(this.index < this.total_page){ // если индекс страницы меньше количества страниц
				this.index += 1 // увеличиваем индекс
			}

			if(this.index === this.total_page){ // если индекс равен количеству страниц
				this.disableNext() // отключаем кнопку вперед
				this.activePrev() // включаем кнопку назад
			}

			this.page_num.textContent = this.index

			this.showByIndex() // отображаем по индексу
		}

		this.disablePrev() // отключаем кнопку назад по дефолту так как индекс начинается с 1
		this.showByIndex() // отображаем по индексу
	}

	showByIndex(){
		// проходимся по всем элементам двумерного массива
		for (var arr of this.items) {
			for (var item of arr) {
				item.classList.remove('show') // удаляем класс для отображения
				item.classList.add('hide') // добавляем класс для скрытия
			}
		}

		for (var item of this.items[this.index-1]) { // выбираем из двумерного массива массив по индексу и проходимя по его элементам
			item.classList.remove('hide') // удаляем класс для скрытия
			item.classList.add('show') // добавляем класс для отображения
		}
	}

	activePrev(){
		this.prev_btn.classList.remove("disabled")
	}

	disablePrev(){
		this.prev_btn.classList.add("disabled")
	}

	activeNext(){
		this.next_btn.classList.remove("disabled")
	}

	disableNext(){
		this.next_btn.classList.add("disabled")
	}
}



var catalog_items = document.querySelectorAll('div.gallery-items div.item')
var pagination = new Pagination(catalog_items, 4)

pagination.init()


let switchMode = document.getElementById("switchMode");
switchMode.onclick =function (){
    let theme = document.getElementById("theme");
    console.log(theme.getAttribute("href"))
    if (theme.getAttribute("href") == "/static/css/Catalog.css"){
        theme.href ="/static/css/CatalogDark.css";
        document.cookie = "theme=dark"
    }
    else{
        theme.href ="/static/css/Catalog.css";
        document.cookie = "theme=light"
    }
}
function answer1(){
	const mbody = document.querySelector(".chatBody");
	let card=
		`<p class="theirMessage bg-warning align-self-end p-3 w-50 d-flex text-start">
		Где располагается наша компания?
	</p>
	<p class="theirMessage bg-dark text-light align-self-start p-3 w-50">
		Мы располагаемся по адресу ул. Советская, 1, Кострома, Костромская обл.
	</p>
	`;
	mbody.insertAdjacentHTML('beforeend', card);
	mbody.scrollTop = mbody.scrollHeight;
}

function answer2(){
	const mbody = document.querySelector(".chatBody");
	let card=
		`<p class="theirMessage bg-warning align-self-end p-3 w-50 d-flex text-start">
		Какое кольцо самое дорогое?
	</p>
	<p class="theirMessage bg-dark text-light align-self-start p-3 w-50">
		Кольцо из белого золота с бриллиантами за  90 000₽ <br> >.<
	</p>
	`;
	mbody.insertAdjacentHTML('beforeend', card);
	mbody.scrollTop = mbody.scrollHeight;
}

function answer3(){
	const mbody = document.querySelector(".chatBody");
	let card=
	`<p class="theirMessage bg-warning align-self-end p-3 w-50 d-flex text-start">
	На каком автобусе можно до вас доехать?
</p>
<p class="theirMessage bg-dark text-light align-self-start p-3 w-50">
	Нуу.. Смотря откуда ехать.. Из-за Волги на 57, из Давыдовского на 4, 51, 56, с Рабочего проспекта тоже на 57!
</p>
`;
	mbody.insertAdjacentHTML('beforeend', card);
	mbody.scrollTop = mbody.scrollHeight;
}

function answer4(){
	const mbody = document.querySelector(".chatBody");
	let card=
		`<p class="theirMessage bg-warning align-self-end p-3 w-50 d-flex text-start">
		Быстро доставляете кольца?
	</p>
	<p class="theirMessage bg-dark text-light align-self-start p-3 w-50">
		Конечно! После покпуки заказ прибудет в течении 2-3 дней
	</p>
	`;
	mbody.insertAdjacentHTML('beforeend', card);
	mbody.scrollTop = mbody.scrollHeight;
}