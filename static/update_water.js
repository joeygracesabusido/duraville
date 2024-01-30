


// this function is for updating Cost Water


const update_cost_water_electric = async () => {
    const id = document.getElementById("transID").value
    const data = {
        sin: document.getElementById("sin_update").value,
        kwt_cubic_meter: document.getElementById("kwt_cubic_meter_update").value,
        amount: document.getElementById("amount_update").value,
       
       
    };
    console.log(data)

    try {
        const response = await fetch(`/update-water-electric-cost/`+ id, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const responseData = await response.json();
        console.log(responseData);
        
        if (responseData.error) {
            // Error occurred on the server side
            if (responseData.error === "Error") {
                window.alert("Error: Error");
            } 
            else {
                window.alert("Error: " + responseData.error);
            }
        }else if (response.status === 401) {
            window.alert("Unauthorized credential. Please login");
        }
         else {
            // Data saved successfully
            window.alert("Your data has been updated!!!!");
            // window.location.assign("/insert-cost/");
        }
       
        
    } catch (error) {
        window.alert(error);
        console.log(error);
    }
};

var Btn_update_cost = document.querySelector('#Btn_update_cost');
Btn_update_cost.addEventListener("click", update_cost_water_electric);
