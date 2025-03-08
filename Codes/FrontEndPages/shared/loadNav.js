(function() {
    'use strict';
    document.addEventListener('DOMContentLoaded', function() {
        const navHTML = `
            <nav class="navbar navbar-expand-lg navbar-light">
                <div class="container">
                    <a class="navbar-brand" href="#">
                        <i class="fas fa-book-quran ms-2"></i>
                        نظام متابعة حفظ القرآن
                    </a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNav">
                        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                            <li class="nav-item">
                                <a class="nav-link" href="index.html"><i class="fas fa-home ms-1"></i> الرئيسية</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="simple.html"><i class="fas fa-users ms-1"></i> الطلاب</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="reports.html"><i class="fas fa-chart-bar ms-1"></i> التقارير</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="settings.html"><i class="fas fa-cog ms-1"></i> الإعدادات</a>
                            </li>
                        </ul>
                        <div class="d-flex">
                            <a href="#" class="btn btn-outline-primary">
                                <i class="fas fa-sign-out-alt ms-1"></i> تسجيل الخروج
                            </a>
                        </div>
                    </div>
                </div>
            </nav>
        `;
        document.getElementById('nav-placeholder').innerHTML = navHTML;
    });
})();