console.log("Test from pagination.js!");
$(document).ready(function() {

    //GET SEARCH FORM AND PAGE LINKS
    let searchForm = document.getElementById('searchForm');
    let pageLinks = Array.from(document.getElementsByClassName('page-link'));

    //ENSURE SEARCH FORM EXISTS
    if (searchForm) {
        pageLinks.forEach(function(pageLink) {
            pageLink.addEventListener('click', function (e) {
                e.preventDefault();

                //GET THE DATA ATTRIBUTE
                let page = this.dataset.page;

                //ADD HIDDEN SEARCH INPUT TO FORM
                let hiddenInput = document.createElement('input');
                hiddenInput.setAttribute('type', 'hidden');
                hiddenInput.setAttribute('name', 'page');
                hiddenInput.setAttribute('value', page);
                searchForm.appendChild(hiddenInput);

                //SUBMIT FORM
                searchForm.submit();
            });
        });
    }
});