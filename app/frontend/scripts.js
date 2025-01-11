document.addEventListener('DOMContentLoaded', () => {
    const fetchEvents = async () => {
      try {
        const response = await fetch('/webhook/ui/data');
        const data = await response.json();
  
        renderTable(data);
      } catch (error) {
        console.error('Error fetching events:', error);
      }
    };
  
    const formatTimestamp = (timestamp) => {
      const date = new Date(timestamp);
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', timeZoneName: 'short' };
      return date.toLocaleString('en-US', options);
    };
  
    const renderTable = (events) => {
      const loader = document.getElementById('loader');
      const table = document.getElementById('events-table');
      const tbody = document.getElementById('events-list');
  
      loader.style.display = 'none';
      table.style.display = 'table';
  
      tbody.innerHTML = '';
  
      events.forEach(event => {
        const row = document.createElement('tr');
  
        let detail;
        switch (event.action) {
          case 'pushed':
            detail = `"${event.author}" pushed to "${event.to_branch}" on ${formatTimestamp(event.timestamp)}`;
            break;
          case 'opened':
          case 'reopened':
            detail = `"${event.author}" submitted a pull request from "${event.from_branch}" to "${event.to_branch}" on ${formatTimestamp(event.timestamp)}`;
            break;
          case 'merged':
            detail = `"${event.author}" merged branch "${event.from_branch}" to "${event.to_branch}" on ${formatTimestamp(event.timestamp)}`;
            break;
          default:
            detail = `"${event.author}" performed an unknown action on ${formatTimestamp(event.timestamp)}`;
        }
  
        const cell = document.createElement('td');
        cell.textContent = detail;
        row.appendChild(cell);
  
        tbody.appendChild(row);
      });
    };
  
    fetchEvents();
    setInterval(fetchEvents, 15000);
  });