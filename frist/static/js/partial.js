
/*
var arabic = document.getElementById("ar"),
    english = document.getElementById("en");
arabic.onclick = function () {

    document.body.classList.add('direction:rtl')

}
english.onclick = function () {

    document.body.classList.add("en");
    document.body.classList.remove("ar")

}
arabic.onclick = function () {

    document.body.classList.add("ar");
    document.body.classList.add("en");
}
*/
/*
var nav11 = document.getElementById("nav1"),
    nav22 = document.getElementById("nav2"),
    nav33 = document.getElementById("nav3");

nav11.onclick = function () {
    nav11.classList.add("active");
    nav22.classList.remove("active");
    nav33.classList.remove("active");
}
nav22.onclick = function () {
    nav22.classList.add("active");
    nav11.classList.remove("active");
    nav33.classList.remove("active");
}
nav33.onclick = function () {
    nav33.classList.add("active");
    nav22.classList.remove("active");
    nav11.classList.remove("active");
}    
*/

window.addEventListener("scroll", function () {
  var nav = document.querySelector("nav");
  nav.classList.toggle("sticky", window.scrollY > 0);
});

("use strict");

const $window = $(window);
const $body = $("body");

class Slideshow {
  constructor(userOptions = {}) {
    const defaultOptions = {
      $el: $(".slideshow"),
      showArrows: false,
      showPagination: true,
      duration: 10000,
      autoplay: true,
    };
    let options = Object.assign({}, defaultOptions, userOptions);
    this.$el = options.$el;
    this.maxSlide = this.$el.find($(".js-slider-home-slide")).length;
    this.showArrows = this.maxSlide > 1 ? options.showArrows : false;
    this.showPagination = options.showPagination;
    this.currentSlide = 1;
    this.isAnimating = false;
    this.animationDuration = 1200;
    this.autoplaySpeed = options.duration;
    this.interval;
    this.$controls = this.$el.find(".js-slider-home-button");
    this.autoplay = this.maxSlide > 1 ? options.autoplay : false;
    this.$el.on("click", ".js-slider-home-next", (event) => this.nextSlide());
    this.$el.on("click", ".js-slider-home-prev", (event) => this.prevSlide());
    this.$el.on("click", ".js-pagination-item", (event) => {
      if (!this.isAnimating) {
        this.preventClick();
        this.goToSlide(event.target.dataset.slide);
      }
    });
    this.init();
  }

  init() {
    this.goToSlide(1);

    if (this.autoplay) {
      this.startAutoplay();
    }

    if (this.showPagination) {
      let paginationNumber = this.maxSlide;
      let pagination = '<div class="pagination"><div class="container">';

      for (let i = 0; i < this.maxSlide; i++) {
        let item = `<span class="pagination__item js-pagination-item ${
          i === 0 ? "is-current" : ""
        }" data-slide=${i + 1}>${i + 1}</span>`;
        pagination = pagination + item;
      }

      pagination = pagination + "</div></div>";
      this.$el.append(pagination);
    }
  }

  preventClick() {
    this.isAnimating = true;
    this.$controls.prop("disabled", true);
    clearInterval(this.interval);
    setTimeout(() => {
      this.isAnimating = false;
      this.$controls.prop("disabled", false);

      if (this.autoplay) {
        this.startAutoplay();
      }
    }, this.animationDuration);
  }

  goToSlide(index) {
    this.currentSlide = parseInt(index);

    if (this.currentSlide > this.maxSlide) {
      this.currentSlide = 1;
    }

    if (this.currentSlide === 0) {
      this.currentSlide = this.maxSlide;
    }

    const newCurrent = this.$el.find(
      '.js-slider-home-slide[data-slide="' + this.currentSlide + '"]'
    );
    const newPrev =
      this.currentSlide === 1
        ? this.$el.find(".js-slider-home-slide").last()
        : newCurrent.prev(".js-slider-home-slide");
    const newNext =
      this.currentSlide === this.maxSlide
        ? this.$el.find(".js-slider-home-slide").first()
        : newCurrent.next(".js-slider-home-slide");
    this.$el
      .find(".js-slider-home-slide")
      .removeClass("is-prev is-next is-current");
    this.$el.find(".js-pagination-item").removeClass("is-current");

    if (this.maxSlide > 1) {
      newPrev.addClass("is-prev");
      newNext.addClass("is-next");
    }

    newCurrent.addClass("is-current");
    this.$el
      .find('.js-pagination-item[data-slide="' + this.currentSlide + '"]')
      .addClass("is-current");
  }

  nextSlide() {
    this.preventClick();
    this.goToSlide(this.currentSlide + 1);
  }

  prevSlide() {
    this.preventClick();
    this.goToSlide(this.currentSlide - 1);
  }

  startAutoplay() {
    this.interval = setInterval(() => {
      if (!this.isAnimating) {
        this.nextSlide();
      }
    }, this.autoplaySpeed);
  }

  destroy() {
    this.$el.off();
  }
}

(function () {
  let loaded = false;
  let maxLoad = 3000;

  function load() {
    const options = {
      showPagination: true,
    };
    let slideShow = new Slideshow(options);
  }

  function addLoadClass() {
    $body.addClass("is-loaded");
    setTimeout(function () {
      $body.addClass("is-animated");
    }, 600);
  }

  $window.on("load", function () {
    if (!loaded) {
      loaded = true;
      load();
    }
  });
  setTimeout(function () {
    if (!loaded) {
      loaded = true;
      load();
    }
  }, maxLoad);
  addLoadClass();
})();



Fancybox.bind('[data-fancybox]', {
  
  clickContent: true,
  clickSlide: false,
  hash: true,
  hideScrollbar: false,
  idleTime: 2000,
  infobar: false,
  loop: true,
});



function copyCurrentLink() {
  // Your copyCurrentLink() function remains unchanged
  var currentLink = document.getElementById('currentLink');
  var textArea = document.createElement('textarea');
  textArea.value = currentLink.innerText;
  document.body.appendChild(textArea);
  textArea.select();
  document.execCommand('copy');
  document.body.removeChild(textArea);

  alert('Current link copied to clipboard!');
}
function showLink() {
  // Set the innerText of 'currentLink' element to the current URL
  document.getElementById('currentLink').innerText = window.location.href;
}


  ///////////////////////////////////////////////////////////////////////
/////////////// no code before here /////////////////////////////////////
///////////////////////////////////////////////////////////////////////

document.addEventListener('DOMContentLoaded', function () {
   // Initialize Splide for spi3
   new Splide('#spi3', {
    type: 'loop',
    perPage: 4,
    focus: 'center',
    autoplay: true,
}).mount();
});
  // Initialize Splide for spi1
  new Splide('.splide.spi1', {
      type: 'loop',
      perPage: 4,
      focus: 'center',
      autoplay: true,
  }).mount();

  // Initialize Splide for spi2
  new Splide('.splide.spi2', {
      type: 'loop',
      perPage: 4,
      focus: 'center',
      autoplay: true,
  }).mount();



// Mount the carousel
///////////////////////////////////////////////////////////////////////
/////////////// code after this /////////////////////////////////////
///////////////////////////////////////////////////////////////////////

