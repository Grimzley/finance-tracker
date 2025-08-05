document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('a[data-scroll]').forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();

        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);

        if (targetElement) {
          const navbarHeight = document.querySelector('.navbar').offsetHeight;
          const elementTop = targetElement.getBoundingClientRect().top;
          const offsetPosition = window.scrollY + elementTop - navbarHeight;

          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
        }
      });
  });
})
