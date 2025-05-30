document.addEventListener('DOMContentLoaded', function() {
  // Toggle sidebar
  const sidebarToggle = document.createElement('button');
  sidebarToggle.classList.add('btn', 'btn-outline-secondary', 'position-fixed');
  sidebarToggle.style.top = '12px';
  sidebarToggle.style.left = '15px';
  sidebarToggle.style.zIndex = '1001';
  sidebarToggle.innerHTML = '<i class="bi bi-list"></i>';
  document.body.appendChild(sidebarToggle);

  const sidebar = document.getElementById('sidebar');
  
  sidebarToggle.addEventListener('click', function() {
    sidebar.classList.toggle('active');
    document.getElementById('content').classList.toggle('expanded');
  });

  // Close sidebar when clicking outside
  document.addEventListener('click', function(event) {
    const targetElement = event.target;
    if (
      sidebar.classList.contains('active') && 
      !sidebar.contains(targetElement) && 
      targetElement !== sidebarToggle && 
      !sidebarToggle.contains(targetElement)
    ) {
      sidebar.classList.remove('active');
      document.getElementById('content').classList.remove('expanded');
    }
  });

  // Handle active page in sidebar
  const sidebarLinks = document.querySelectorAll('#sidebar a');
  
  sidebarLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      // Remove active class from all parent li elements
      sidebarLinks.forEach(link => {
        link.parentElement.classList.remove('active');
      });
      
      // Add active class to clicked link's parent li
      this.parentElement.classList.add('active');
      
      // Store active page in localStorage
      localStorage.setItem('activePage', this.getAttribute('href'));
    });
  });

  // Add hover effect to dashboard cards
  const infoCards = document.querySelectorAll('.info-card');
  
  infoCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-5px)';
      this.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.1)';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
      this.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.05)';
    });
  });

  // Example function to add an announcement
  window.addAnnouncement = function(title, content, date) {
    const announcementsContainer = document.querySelector('.announcement-item');
    announcementsContainer.innerHTML = '';
    
    const announcementElement = document.createElement('div');
    announcementElement.classList.add('announcement');
    
    announcementElement.innerHTML = `
      <h5>${title}</h5>
      <p>${content}</p>
      <small class="text-muted">${date}</small>
    `;
    
    announcementsContainer.appendChild(announcementElement);
  };

  // Example function to update current term and week
  window.updateTermInfo = function(term, week) {
    const termInfoElement = document.querySelector('.welcome-content p:last-child');
    termInfoElement.textContent = `It is currently Term ${term} Week ${week}.`;
  };

  // Display current date in a more user-friendly format
  const displayCurrentDate = function() {
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const dateString = now.toLocaleDateString('en-US', options);
    
    const dateElement = document.createElement('p');
    dateElement.classList.add('current-date', 'text-white', 'opacity-75', 'mb-0');
    dateElement.textContent = dateString;
    
    const welcomeContent = document.querySelector('.welcome-content');
    welcomeContent.appendChild(dateElement);
  };
  
  displayCurrentDate();
});