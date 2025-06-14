async function createNFT() {
  try {
    const response = await fetch('http://localhost:5000/create_nft', { method: 'POST' });
    console.log(response);
    const data = await response.json();
    document.getElementById("nft-status").innerText = data.message;
  } catch (err) {
    document.getElementById("nft-status").innerText = "Error: " + err.message;
  }
}

async function checkWhitelist() {
  const teamId = document.getElementById("teamId").value;
  try {
    const response = await fetch(`http://localhost:5000/check_whitelist/${teamId}`);
    const data = await response.json();
    document.getElementById("whitelist-result").innerText = data.message;
  } catch (err) {
    document.getElementById("whitelist-result").innerText = "Error: " + err.message;
  }
}

async function buyNFT() {
  const input = document.getElementById("mnemonics").value;
  const mnemonics = input.split(",").map(m => m.trim());

  console.log(mnemonics);

  if (mnemonics.length < 2) {
    alert("Please enter 2 mnemonics");
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/buy_nft", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mnemonics: mnemonics })
    });
    const data = await response.json();
    console.log(data);
    document.getElementById("buy-status").innerText = data.message;
  } catch (err) {
    document.getElementById("buy-status").innerText = "Error: " + err.message;
  }
}
