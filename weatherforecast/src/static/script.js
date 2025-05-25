async function send(last_city=null){

    document.getElementById("id_weather").textContent = `Weather: ...`

    let city;

    if (last_city){
        city = last_city
    }
    else{
        city = document.getElementById("city").value;
    }

    const response = await fetch("/weather", {
            method: "POST",
            headers: { "Accept": "application/json", "Content-Type": "application/json" },
            body: JSON.stringify({
                city: city
            })
        });
        if (response.ok) {
            const data = await response.json();

            let current_weather = data.Current_weather
            let current_weather_units = data.Current_weather_units

            document.getElementById("id_weather").textContent = `Weather: ${current_weather}${current_weather_units}`
        }
        else
            console.log(response);
}

async function suggest_city(){

    const city = document.getElementById("city").value;
    const suggestionsBox = document.getElementById("suggestions");
    suggestionsBox.innerHTML = "";

    const response = await fetch("/suggest_city", {
            method: "POST",
            headers: { "Accept": "application/json", "Content-Type": "application/json" },
            body: JSON.stringify({
                city: city
            })
        });
        if (response.ok) {
            const data = await response.json();

            data.forEach(city => {
                const div = document.createElement("div");
                div.innerText = `${city.name}, ${city.country}, ${city.lat}, ${city.lon}`;
                div.onclick = () => {
                    document.getElementById("city").value = `${city.name}, ${city.country}, ${city.lat}, ${city.lon}`;
                    suggestionsBox.innerHTML = "";
                };
                suggestionsBox.appendChild(div);
            });
        }
        else
            console.log(response);
}