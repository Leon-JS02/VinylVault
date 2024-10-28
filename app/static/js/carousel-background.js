document.addEventListener('DOMContentLoaded', function () {
    const carouselElement = document.getElementById('albumCarousel');
    const backgroundContainer = document.querySelector('.background-container');

    function updateBackground() {
        const activeItem = carouselElement.querySelector('.carousel-item.active img');
        if (activeItem) {
            const imageUrl = activeItem.src;
            backgroundContainer.style.backgroundImage = `url(${imageUrl})`;
        }
    }
    updateBackground();
    carouselElement.addEventListener('slid.bs.carousel', updateBackground);
});
