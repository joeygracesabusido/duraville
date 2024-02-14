// this function is to insert branch
const insert_branch = async () => {
    const data = {
        branch_code: document.getElementById("insert_branch_input").value
    };
    
    try {
        const response = await fetch(`/api-insert-branch-cost/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            const responseData = await response.json();
            console.log(responseData);
            // Data saved successfully
            window.alert("Your data has been saved!!!!");
            // Optionally, you can redirect to another page
            window.location.assign("/dashboard/");
        } else if (response.status === 401) {
            // Unauthorized, session has expired
            window.alert("Session has expired");
        } else if (response.status === 400) {
            // Bad Request, duplicate branch
            const responseData = await response.json();
            window.alert(`Error: ${responseData.detail}`);
        } else {
            // Handle other errors
            window.alert("An unexpected error occurred");
        }
    } catch (error) {
        // Handle unexpected errors
        window.alert("An unexpected error occurred");
        console.log(error);
    }
};

// Attach the event listener to the button
var Btn_branch_save = document.querySelector('#Bnt_save_branch');
Btn_branch_save.addEventListener("click", insert_branch);

// this function is for autocomplete of branch
jQuery(document).ready(function() {
    jQuery("#branch_insert_cost_input2").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/api-search-autocomplete-branch/",
                data: { term: request.term },
                dataType: "json",
                success: function(data) {
                    response(data);
                }
            });
        },
        select: function(event, ui) {
            $("#branch_insert_cost_input2").val(ui.item.value);
            // $("#rentalRateInsertRental").val(ui.item.rentalRate);
            
            return false;
        }
    });
});


function initializeAutocomplete() {
    $("#branch_insert_cost_input").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/api-search-autocomplete-branch/",
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
            $("#branch_insert_cost_input").val(ui.item.value);
            if (ui.item.value === 'ELECTRICITY'){
                // $("#insert_cost").modal("hide");
                // $("#electricity_water_form").modal("show");
            }

            
            return false;
        }
    });
  }


   // Open modal and initialize autocomplete when the button is clicked
$("#btn_insert_cost").on("click", function() {
    $("#modal-electricity-graph").modal("show");  // Adjust modal ID as needed
    initializeAutocomplete();  // Initialize autocomplete when the modal is shown
  });



//   $(document).ready(function () {
//     $('#my_table_cost').DataTable();
// });


  // Open modal and initialize autocomplete when the button is clicked
// $("#edit_water_electricity").on("click", function() {
//     $("#electricity_water_form").modal("show");  // Updated modal ID
//   });


// this  function is to insert cost elements

// Arrow function to log a message


// const logMessage = () => {
//     console.log("I'm alive!");
// };

// // Attach the event listener to the "Save" button
// const Btn_save_cost = document.querySelector('#Btn_insert_costElement2');
// Btn_save_cost.addEventListener("click", logMessage);



const insert_cost_EL = async () => {

    
    const data = {
        cost: document.getElementById("cost_elements_insert").value
    };

    console.log(data)
    
    try {
        const response = await fetch(`/api-insert-cost-elements/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            const responseData = await response.json();
            console.log(responseData);
            // Data saved successfully
            window.alert("Your data has been saved!!!!");
            // Optionally, you can redirect to another page
            window.location.assign("/dashboard/");
        } else if (response.status === 401) {
            // Unauthorized, session has expired
            window.alert("Session has expired");
        } else if (response.status === 400) {
            // Bad Request, duplicate branch
            const responseData = await response.json();
            window.alert(`Error: ${responseData.detail}`);
        } else {
            // Handle other errors
            window.alert("An unexpected error occurred");
        }
    } catch (error) {
        // Handle unexpected errors
        window.alert("An unexpected error occurred");
        console.log(error);
    }
};

// Attach the event listener to the button
const Btn_save_cost2 = document.querySelector('#Btn_insert_costElement');
Btn_save_cost2.addEventListener("click", insert_cost_EL);



$(document).ready(function() {
   
    $.ajax({
        url: '/api-get-electricty-graph',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            // Process the received data and create the bar graph
            createElectricityGraph(data);
        },
        error: function(error) {
            console.error('Error fetching data:', error);
        }
    });

   
    // Function to create the bar graph
    function createElectricityGraph(data) {
        var labels = data.map(item => item.person_incharge_end_user);
        var values = data.map(item => item.khw_no);
        console.log()
        var ctx = document.getElementById('electricityChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Electricity Graph',
                    data: values,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }


    // Function to show the modal and create the graph
    function showElectricityModal() {
        $("#elec-graph").modal("show");
        createElectricityGraph(data);
    }


    $("button[data-target='#electric_graph']").on("click", showElectricityModal);


});






