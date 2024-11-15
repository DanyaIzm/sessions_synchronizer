const socket = new WebSocket(`ws://${location.host}/ws`);

const tableBody = document.querySelector(".clients-table__body");

socket.onopen = () => {
  const clientsUpdateInterval = setInterval(() => {
    socket.send("get_all_sessions");
  }, 2000);

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    tableBody.innerHTML = "";

    data.forEach((client) => {
      tableBody.innerHTML += `
      <tr>
            <td class="clients-table__cell">${client.id.split("-").shift()}</td>
            <td class="clients-table__cell">${client.start_time}</td>
            <td class="clients-table__cell">${client.duration}</td>
            <td class="clients-table__cell clients-table__cell__address">${
              client.address
            }</td>
            <td class="clients-table__cell">${client.user_agent}</td>
      </tr>
      `;
    });
  };

  socket.onclose = () => {
    clearInterval(clientsUpdateInterval);

    const connectionLostBlock = document.querySelector(".connection-lost");

    connectionLostBlock.classList.remove("inactive");
  };

  socket.send("get_all_sessions");
};
