
// this function is for updating Cost Water


const update_cost_water_electric = async () => {
    const id = document.getElementById("transID").value
    const data = {
        sin: document.getElementById("sin").value,
        can: document.getElementById("can").value,
        khw_no: document.getElementById("khw_no").value,
        price: document.getElementById("price").value,
        cubic_meter: document.getElementById("cubic_meter").value,
        pic: document.getElementById("pic").value,
        person_incharge_end_user: document.getElementById("person_incharge_end_user").value,
        no_of_person: document.getElementById("no_of_person").value,
        activity_made: document.getElementById("activity_made").value,
        plate_no: document.getElementById("plate_no").value,
        cost_elements: document.getElementById("cost_elements").value,
        liters: document.getElementById("liters").value,
        type_of_vehicle: document.getElementById("type_of_vehicle").value,
       
    };
    console.log(data)

    try {
        const response = await fetch(`/update-cost/`+ id, {
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


// this is for autocomple for Cost Elements


$(document).ready(function() {
    $("#cost_elements").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/api-search-autocomplete-cost-elements/",
                data: { term: request.term },
                dataType: "json",
                success: function(data) {
                    response(data);
                },
                error: function(err) {
                    console.log("Error fetching autocomplete data:", err);
                }
            });
        },
        minLength: 2,  // Minimum length of the input before triggering autocomplete
        select: function(event, ui) {
            $("#cost_elements").val(ui.item.value);
            
            return false;
        }
    });
});
