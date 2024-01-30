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

// // this function is for autocomplete of branch
$(document).ready(function() {
    $("#branch_insert_cost_input2").autocomplete({
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
    $("#modal_insert_cost").modal("show");  // Adjust modal ID as needed
    initializeAutocomplete();  // Initialize autocomplete when the modal is shown
  });


  $(document).ready(function () {
    $('#my_table_cost').DataTable();
});


  // Open modal and initialize autocomplete when the button is clicked
// $("#edit_water_electricity").on("click", function() {
//     $("#electricity_water_form").modal("show");  // Updated modal ID
//   });
  



