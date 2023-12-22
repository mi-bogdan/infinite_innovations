document.addEventListener('DOMContentLoaded', function () {
  var sliderContent = document.querySelector('.slider-content');
  var prevButton = document.querySelector('.prev-button');
  var nextButton = document.querySelector('.next-button');
  var slides = document.querySelectorAll('.slide');
  var currentSlide = 0;

  function goToSlide(n) {
    sliderContent.style.transform = 'translateX(-' + (n * 100) + '%)';
    currentSlide = n;
  }

  function goToNextSlide() {
    if (currentSlide < slides.length - 1) {
      goToSlide(currentSlide + 1);
    } else {
      goToSlide(0);
    }
  }

  function goToPrevSlide() {
    if (currentSlide > 0) {
      goToSlide(currentSlide - 1);
    } else {
      goToSlide(slides.length - 1);
    }
  }

  nextButton.addEventListener('click', function (e) {
    e.preventDefault();
    goToNextSlide();
  });

  prevButton.addEventListener('click', function (e) {
    e.preventDefault();
    goToPrevSlide();
  });
});

function toggleModal() {
  var modal = document.getElementById("loginModal");
  modal.style.display = modal.style.display === "block" ? "none" : "block";
}



// ========================================================================================================================

// Получаем элементы
var modal = document.getElementById("saveModal");
var btn = document.getElementById("saveLink");
var span = document.getElementsByClassName("close")[0];

// Открытие модального окна при клике на ссылку
btn.onclick = function(event) {
    event.preventDefault(); // Предотвращаем переход по ссылке
    modal.style.display = "block";
}

// Закрытие модального окна при клике на (x) 
span.onclick = function() {
    modal.style.display = "none";
}

// Закрытие модального окна при клике вне его области
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}


