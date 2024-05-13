$(document).ready(function() {
    $("#name").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/api-acutocomplte-employee/",
                data: { term: request.term },
                dataType: "json",
                success: function(data) {
                    response(data);
                },
                error: function(err) {
                    console.error("Error fetching autocomplete data:", err);
                    // Optionally, provide user feedback about the error
                }
            });
        },
        minLength: 0,  // Minimum length of the input before triggering autocomplete
        select: function(event, ui) {
            $("#name").val(ui.item.value);
            
            $("#employee_id_id").val(ui.item.id);

            return false;
        }
    });

  
});


// this function is to insert allowance
// Arrow function to handle form submission
const insert_allowance = () => {
    // Get form values
    const payroll_date = $("#payroll_date").val();
    const name = $("#name").val();
    const allowance = $("#allowance").val();
    const meal_allowance = $("#meal_allowance").val();
    const developmental = $("#developmental").val();
    const holiday_rdot_pay = $("#holiday_rdot_pay").val();
    const allowance_deduction = $("#allowance_deduction").val();
    const allowance_adjustment = $("#allowance_adjustment").val();
    const employee_id_id = $("#employee_id_id").val();

    // Send data to GraphQL endpoint using AJAX
    $.ajax({
      url: '/your-graphql-endpoint',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        query: `
          mutation {
            insert_allowance(
              employee_id_id: ${employee_id_id},
              allowance: ${allowance},
              meal_allowance: ${meal_allowance},
              developmental: ${developmental},
              holiday_rdot_pay: ${holiday_rdot_pay},
              allowance_deduction: ${allowance_deduction},
              allowance_adjustment: ${allowance_adjustment},
              payroll_date: "${payroll_date}",
              user: "${name}"
            )
          }
        `
      }),
      success: (response) => {
        // Handle success response
        console.log(response);
        // Optionally, display a success message to the user
      },
      error: (error) => {
        // Handle error response
        console.error(error);
        // Optionally, display an error message to the user
      }
    });
  };

  // Event listener for form submission
  $(document).ready(() => {
    $("#btn_save_allowance").click((event) => {
      event.preventDefault(); // Prevent default form submission
      insert_allowance(); // Call the submitForm function
    });
  });


// this function is to display data of allowance


$(document).ready(function() {
    $.ajax({
        type: 'POST',
        url: '/graphql', // Change this to your GraphQL endpoint
        contentType: 'application/json',
        data: JSON.stringify({
            query: `query MyQuery {
                getAllowanceList {
                  payrollDate
                  name
                  allowance
                  mealAllowance
                  developmental
                  holidayRdotPay
                  allowanceAdjustment
                  allowanceDeduction
                }
              }`
        }),
        success: function(response) {
            var data = response.data.getAllowanceList;
            var tableBody = $('#my_table_allowance');
            tableBody.empty();

            data.forEach(function(item) {
                var formattedAllowance = parseFloat(item.allowance).toLocaleString(undefined, {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                });
                var row = '<tr>' +
                    '<td>' + item.payrollDate + '</td>' +
                    '<td>' + item.name + '</td>' +
                    '<td>' + formattedAllowance + '</td>' +
                    '<td>' + item.mealAllowance + '</td>' +
                    '<td>' + item.developmental + '</td>' +
                    '<td>' + item.holidayRdotPay + '</td>' +
                    '<td>' + item.allowanceDeduction + '</td>' +
                    '<td>' + item.allowanceAdjustment + '</td>' +
                    '</tr>';
                tableBody.append(row);
            });

            initializeDataTable();
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });
});

const initializeDataTable = () => {
    $('#my_table_allowance2').DataTable();
};
