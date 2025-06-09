$(document).ready(function () {
    const $sidebar = $('#sidebar');
    const $mainContent = $('#mainContent');
    const $mainFooter = $('#mainFooter');
    const $toggleIconTop = $('#sidebarToggleTop').find('i');
    const $toggleIconBottom = $('#sidebarToggleBottom').find('i');
    let sidebarCollapsed = `{{=session.btn_sidebar}}`;
    console.log(sidebarCollapsed)

    function toggleSidebar() {
        $sidebar.toggleClass('collapsed');
        $mainContent.toggleClass('collapsed');
        $mainFooter.toggleClass('collapsed');
        sidebarCollapsed = $sidebar.hasClass('collapsed');
        $('#sidebarToggleBottom').val(sidebarCollapsed)
        if ($sidebar.hasClass('collapsed')) {
            $toggleIconTop.removeClass('fa-angle-double-left').addClass('fa-angle-double-right');
            $toggleIconBottom.removeClass('fa-angle-double-left').addClass('fa-angle-double-right');
        } else {
            $toggleIconTop.removeClass('fa-angle-double-right').addClass('fa-angle-double-left');
            $toggleIconBottom.removeClass('fa-angle-double-right').addClass('fa-angle-double-left');
        }
    }

    function widthChangeDetect() {
        $(window).resize(function() {
            var width = $(window).width();
            setTimeout(function () {
                $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
                const main = document.getElementById('mainContent');
                main.style.display = 'none';
                main.offsetHeight; // trigger reflow
                main.style.display = '';
            }, 300);
        });
    }

    widthChangeDetect();

    // Add event listeners for both top and bottom toggle buttons
    $('#sidebarToggleTop, #sidebarToggleBottom').on('click', function () {
        $('#dataTable').DataTable().columns.adjust().draw();
        $('#dataTable').DataTable().destroy();
        $('#dataTable').DataTable({
            paging: false,
            info: false,
            searching: false,
        });

        toggleSidebar();
        /*setTimeout(function () {
            $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust();
            const main = document.getElementById('mainContent');
            main.style.display = 'none';
            main.offsetHeight; // trigger reflow
            main.style.display = '';
        }, 300);*/
    });

    // Hide sidebar on mobile after clicking a non-dropdown link
    $('.sidebar .nav-link').on('click', function () {
        if (window.innerWidth < 768 && !$(this).attr('data-bs-toggle')) {
            $sidebar.addClass('collapsed');
            $mainContent.removeClass('collapsed');
            $mainFooter.removeClass('collapsed');
            $toggleIconTop.removeClass('fa-angle-double-left').addClass('fa-angle-double-right');
            $toggleIconBottom.removeClass('fa-angle-double-left').addClass('fa-angle-double-right');
        }
    });

    // floating 
    $('#menuToggle').on('click', function (e) {
        e.stopPropagation(); // Prevent bubbling to document
        $('#floatingMenu').toggleClass('show');
    });

    // Optional: Auto-collapse when clicking outside
    $(document).on('click', function (e) {
        if (!$(e.target).closest('#floatingMenu, #menuToggle').length) {
            $('#floatingMenu').removeClass('show');
        }
    });
});