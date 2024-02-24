
var th = ['','Thousand','Million','Billion','Trillion'];
    var dg = ['Zero','One','Two','Three','Four',
              'Five','Six','Seven','Eight','Nine'];
    var tn = ['Ten','Eleven','Twelve','Thirteen', 'Fourteen','Fifteen','Sixteen',
              'Seventeen','Sighteen','Nineteen'];
    var tw = ['Twenty','Thirty','Forty','Fifty',
              'Sixty','Seventy','Eighty','Ninety'];
  
    function toWords(s) {
      s = s.toString();
      s = s.replace(/[\, ]/g,'');
  
      if (s != parseFloat(s)) return 'not a number';
  
      var x = s.indexOf('.');
      if (x == -1) x = s.length;
  
      if (x > 15) return 'too big';
  
      var n = s.split('');
      var str = '';
      var sk = 0;
  
      for (var i = 0; i < x; i++) {
        if ((x - i) % 3 == 2) {
          if (n[i] == '1') {
            str += tn[Number(n[i+1])] + ' ';
            i++;
            sk = 1;
          } else if (n[i] != 0) {
            str += tw[n[i] - 2] + ' ';
            sk = 1;
          }
        } else if (n[i] != 0) {
          str += dg[n[i]] + ' ';
          if ((x - i) % 3 == 0) str += 'hundred ';
          sk = 1;
        }
  
        if ((x - i) % 3 == 1) {
          if (sk) str += th[(x - i - 1) / 3] + ' ';
          sk = 0;
        }
      }
  
      if (x != s.length) {
        var y = s.length;
        str += 'and ';
  
        for (var i = x + 1; i < y; i++) {
          str += dg[n[i]] + ' ';
        }
      }
  
      return str.replace(/\s+/g,' ');
    }
  
    function decimalToFraction(decimalPart) {
        if (decimalPart === 0) return '';

        const epsilon = 1e-15;
        const numerator = Math.round(decimalPart * 100 + epsilon);
        const denominator = 100;

        return `${numerator}/${denominator}`;
        }


        document.getElementById("payable_amount").addEventListener("input", function () {
        const inputNumber = parseFloat(this.value) || 0;
        const integerPart = Math.floor(inputNumber);
        const decimalPart = inputNumber - integerPart;

        const spelledIntegerPart = toWords(integerPart);
        const spelledDecimalPart = decimalToFraction(decimalPart);

        const spelledNumber = spelledIntegerPart + (decimalPart ? ` and ${spelledDecimalPart}` : '');

        document.getElementById("spell_number").value = spelledNumber;
        });


// this function is for computation of 
$(document).ready(function() {
    $('#net_of_vat, #non_vat_amount,#vat_amount').on('input', function() {
        calculateAmount2();
    });
    });

    function calculateAmount2() {
    let product
    var net_of_vat_comp = $('#net_of_vat').val() || 0;
    var non_vat_comp = $('#non_vat_amount').val() || 0 ;
    let expanded_withheld_comp = $('#non_vat_amount').val() || 0 ;
    let vat_amount = $('#vat_amount').val() || 0;
    let gross_amount;
    
    
    
    product = parseFloat(net_of_vat_comp) + parseFloat(non_vat_comp);
    expanded_withheld_comp = parseFloat(product) * .02
    gross_amount = parseFloat(product) + parseFloat(vat_amount)
    payable_amount = parseFloat(gross_amount) - parseFloat(expanded_withheld_comp)
    // product = product.toFixed(2)
    // var formattedAmount = product.toLocaleString("en-US", { style: "currency", currency: "USD" });
    const stringNumber2 = product.toFixed(2)
    const expanded_comp = expanded_withheld_comp.toFixed(2)
    const payable_amount_comp = payable_amount.toFixed(2)
    const gross_amount_comp = gross_amount.toFixed(2)
    
    
    $('#total_amount').val(stringNumber2);
    $('#with_holdingtax').val(expanded_comp);
    $('#gross_amount').val(gross_amount_comp)
    $('#payable_amount').val(payable_amount_comp);
     

    // Call the decimalToFraction function with the decimal part of payable_amount
    const decimalPart = payable_amount - Math.floor(payable_amount);
    const spelledDecimalPart = decimalToFraction(decimalPart);

    // Use toWords function for integer part of payable_amount
    const spelledIntegerPart = toWords(Math.floor(payable_amount));

    const spelledNumber = spelledIntegerPart + (decimalPart ? ` and ${spelledDecimalPart}` : '');

    // Set the value in the 'spell_number' element
    document.getElementById("spell_number").value = spelledNumber;
    }

    

    document.getElementById("payable_amount").addEventListener("input", function() {
 
    
    }

);


// Open modal and initialize autocomplete when the button is clicked
$("#btn_insert_electric_data").on("click", function() {
  $("#electric_modal").modal("show");  // Adjust modal ID as needed
 
});

//  Open Modal for Meralco Info
$("#btn_meralco_info").on("click", function() {
  $("#meralco_info").modal("show");  // Adjust modal ID as needed
  initializeAutocomplete_books()
 
});


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
      var ctx = document.getElementById('myChart').getContext('2d');
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
 });


 function initializeAutocomplete_books() {
  $("#book_meralco_info").autocomplete({
      source: function(request, response) {
          $.ajax({
              url: "/api-search-autocomplete-books/",
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
          $("#book_meralco_info").val(ui.item.value);
          $("#company_id_meralco_info").val(ui.item.company_id);
          $("#book_id_meralco_info").val(ui.item.id);

          
          return false;
      }
  });
}

// this function is to insert 
const insert_meralco_details = async () => {
    const data = {
        company_id: document.getElementById("company_id_meralco_info").value,
        customer_account_no: document.getElementById("can_no_meralco_details").value,
        service_id_no: document.getElementById("sin_no_meralco_details").value,
        book_id: document.getElementById("book_id_meralco_info").value,
        end_user: document.getElementById("end_user_meralco_info").value,
        subject_to_ewt: document.getElementById("subject_to_ewt_meralco_info").value,
        

    };
    
    try {
        const response = await fetch(`/api-insert-meralco-details/`, {
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
        } 
        else if (response.status === 500) {
            // Unauthorized, session has expired
            window.alert("Duplicate Entry");
        } 
        else if (response.status === 400) {
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

var Btn_save_electric_details = document.querySelector('#Btn_save_electricity_details');
Btn_save_electric_details.addEventListener("click", insert_meralco_details);


 
 




