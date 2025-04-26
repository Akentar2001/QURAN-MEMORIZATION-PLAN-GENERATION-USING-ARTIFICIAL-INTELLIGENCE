(function() {
    'use strict';
    document.addEventListener('DOMContentLoaded', function() {
        const navHTML = `
            <nav class="navbar navbar-expand-lg navbar-light">
                <div class="container">
                    <a class="navbar-brand d-flex align-items-center" href="../HTML/home.html" style="gap: 8px;"> 
                        <img src="../images/logo.png" alt="Logo" style="width: 60px; height: 60px;">
                        <div class="d-flex flex-column justify-content-center">
                            <span class="fw-bold" style="font-size: 1.8rem; color: #0d6efc">متقن</span>
                            <span class="text-muted" style="font-size: 1rem;">لإنشاء خطط لحفظ القرآن الكريم</span>
                        </div>
                    </a>

                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNav">
                        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                            <!-- Comment
                            <li class="nav-item">
                                <a class="nav-link" href="index.html"><i class="fas fa-home ms-1"></i> الرئيسية</a>
                            </li>
                            -->
                            <li class="nav-item">
                                <a class="nav-link" href="../HTML/home.html"><i class="fas fa-users ms-1"></i> الطلاب</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="../HTML/StudentEvaluation.html"><i class="fas fa-chart-bar ms-1"></i>تقييم الطلاب</a>
                            </li>
                            <!-- Comment
                            <li class="nav-item">
                                <a class="nav-link" href="settings.html"><i class="fas fa-cog ms-1"></i> الإعدادات</a>
                            </li>
                            -->
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