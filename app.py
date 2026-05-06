async function me() {
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Token não encontrado");
        return;
    }

    try {
        const res = await fetch("/me", {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        if (!res.ok) {
            throw new Error("Erro HTTP: " + res.status);
        }

        const data = await res.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        const userInfo = document.getElementById("userInfo");

        if (userInfo) {
            userInfo.innerText =
                `Nome: ${data.name} | Saldo: ${data.balance}`;
        }

    } catch (err) {
        console.error(err);
        alert("Erro ao atualizar sessão");
    }
}
