const buttons = document.querySelectorAll(".btn2");

buttons.forEach((button) => {
  button.addEventListener("mouseenter", () => {
    buttons.forEach((btn) => {
      if (btn !== button) {
        btn.classList.add("hidden");
      }
    });
  });

  button.addEventListener("mouseleave", () => {
    buttons.forEach((btn) => {
      btn.classList.remove("hidden");
    });
  });
});

document
  .getElementById("searchForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    const searchTerm = document
      .getElementById("searchInput")
      .value.toLowerCase();
    if (searchTerm === "") {
      alert("Пожалуйста, введите ключевое слово для поиска!");
      return;
    }

    // Удаляем старые выделения
    removeHighlights();

    // Ищем и подсвечиваем ключевые слова
    const found = highlightText(searchTerm);

    // Прокручиваем к первому найденному результату
    if (found) {
      scrollToFirstHighlight();
    } else {
      alert("Ключевое слово не найдено!");
    }
  });

function highlightText(searchTerm) {
  let found = false;

  // Находим все элементы на странице, в которых может быть текст
  const bodyTextNodes = document.body.querySelectorAll(
    "p, h1, h2, h3, h4, h5, h6, li, span, a, div"
  );

  bodyTextNodes.forEach((node) => {
    // Ищем в тексте узла совпадение с ключевым словом
    if (node.innerHTML.toLowerCase().includes(searchTerm)) {
      const regex = new RegExp(`(${searchTerm})`, "gi");
      node.innerHTML = node.innerHTML.replace(
        regex,
        '<span class="highlighted">$1</span>'
      );
      found = true;
    }
  });

  return found;
}

function removeHighlights() {
  // Убираем старые выделения
  const highlightedElements = document.querySelectorAll(".highlighted");
  highlightedElements.forEach((el) => {
    el.outerHTML = el.innerHTML; // Убираем выделение
  });
}

function scrollToFirstHighlight() {
  // Ищем первый элемент с классом "highlighted"
  const firstHighlight = document.querySelector(".highlighted");

  if (firstHighlight) {
    // Прокручиваем к элементу с эффектом плавной прокрутки
    firstHighlight.scrollIntoView({
      behavior: "smooth",
      block: "center", // Позиционируем его в центре экрана
      inline: "nearest",
    });
  }
}

// Получаем элемент header
const header = document.querySelector("header");

// Слушаем событие прокрутки
window.addEventListener("scroll", () => {
  // Проверяем, сколько пикселей прокручено
  if (window.scrollY > 1400) {
    // Если прокручено больше 1000px, скрываем шапку
    header.classList.add("hidden");
  } else {
    // Если прокручено меньше 1000px, показываем шапку
    header.classList.remove("hidden");
  }
});
