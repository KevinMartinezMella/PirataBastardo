$(document).ready(function(){
    $('.contene2r').hide();
})

function cargador(){
    $('.contene2r').show();
}

$('.carruselPrincipal').slick({
    dots: true,
    infinite: false,
    arrows: false,
    autoplay: true,
    focusOnSelect: true,
    pauseOnHover:false,
    autoplaySpeed: 3000,
});

$('.ultimos').slick({
    dots: false,
    infinite: true,
    arrows: true,
    autoplay: true,
    focusOnSelect: true,
    pauseOnHover:false,
    autoplaySpeed: 2500,
    slidesToShow: 6,
    slidesToScroll: 1,
    responsive: [
        {
          breakpoint: 1200,
          settings: {
            slidesToShow: 4,
            slidesToScroll: 1,
          },
        },
        {
          breakpoint: 1008,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 1,
          },
        },
        {
          breakpoint: 800,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 1,
          },
        },
        {
            breakpoint: 500,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
            },
          },
      ],
});