// this is for autocomplete using graphql

$( function() {
    function split( val ) {
      return val.split( /,\s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }
    
    $("#name").autocomplete({
      source: function( request, response ) {
        $.ajax({
          url: "/graphql",
          dataType: "json",
          data: {
            query: `
              query {
                getEmployeeWithDeductions2(term: "${extractLast(request.term)}") {
                  name
                  totalCashAdvance
                  totalHdmfLoanDeduction
                  totalSssLoanDeduction
                  id
                  basicMonthlyPay
                  books
                }
              }
            `
          },
          success: function( data ) {
            response( data.data.getEmployeeWithDeductions2.map(function(item) {
              return {
                label: item.name,
                value: item.name,
                id: item.id,
                basicMonthlyPay: item.basicMonthlyPay,
                totalCashAdvance: item.totalCashAdvance,
                totalSssLoanDeduction: item.totalSssLoanDeduction,
                totalHdmfLoanDeduction: item.totalHdmfLoanDeduction,
                books: item.books
              };
            }));
          }
        });
      },
      minLength: 2,
      select: function( event, ui ) {
        $("#name").val(ui.item.value);
        $("#employee_id_id").val(ui.item.id);
        $("#basic_pay").val(ui.item.basicMonthlyPay / 2);
       
        $("#books").val(ui.item.books);

        const basicPayValue = $("#basic_pay").val();
        console.log(basicPayValue);

        calculatetotalGross();
        BtnMandatory();
        calculatetotalDeduction();
       
       
        return false;
      }
    });
  });



  // this is for autocomplete of sss

 
    function BtnMandatory() {
      const searchBasicPay = ($("#basic_pay").val()) * 2; // Get the value of the input field
      const getSSSQuery = `
        query {
          getSssTable(amount: ${searchBasicPay}) {
            employeeShares
            employerShare
            ssProvidentEmp
            ssProvidentEmpr
            ecc
          }
        }
      `;
  
      $.ajax({
        url: "/graphql",
        method: "POST",
        data: JSON.stringify({ query: getSSSQuery }),
        contentType: "application/json",
        success: function(data) {
          const empshares = data.data.getSssTable.map(item => item.employeeShares);
          const ssProvidentEmp = data.data.getSssTable.map(item => item.ssProvidentEmp);
          $("#sss").val(empshares);
          $("#sss_provident").val(ssProvidentEmp);

          

          let basicPayValue = $("#basic_pay").val();
          let phic_com;
          let hdmf_comp;

          hdmf_comp = 200
          if ((basicPayValue * 2) <= 10000){
            phic_com =  500 / 2
            phic_come = phic_com.toFixed(2)
            $("#phic").val(phic_come);
          } else{
            phic_com =  (basicPayValue * 2) * 0.05 / 2
            phic_come = phic_com.toFixed(2)
            $("#phic").val(phic_come);
          }
          
          $("#hdmf").val(hdmf_comp);

          
        },
        error: function(xhr, status, error) {
          console.error("Request failed:", error);
        }
      });
    }




  // // Or call the function when a button is clicked
  // $("#search_button").on("click", function() {
  //   BtnMandatory();
  // });
  
  
  
  


// this is for computation of gross payroll
  $(document).ready(function() {
    $('#basic_pay,#late,#absent,#under_time,#normal_working_day_ot, \
        #holiday_ot,#basic_pay_adjustment,#spl_30,#legal_holiday').on('input', function() {
        calculatetotalGross();
        calculatetotalDeduction()
    });
    });

    function calculatetotalGross() {
    
    let basic_pay;
    let late;
    let absent;
    let under_time;
    let normal_working_day_ot;
    let holiday_ot;
    let basic_pay_adjustment;
    let spl_30;
    let legal_holiday;
   


    basic_pay = $('#basic_pay').val() || 0;
    late = $('#late').val() || 0;
    absent = $('#absent').val() || 0;
    under_time = $('#under_time').val() || 0;
    normal_working_day_ot = $('#normal_working_day_ot').val() || 0;
    holiday_ot = $('#holiday_ot').val() || 0;
    basic_pay_adjustment = $('#basic_pay_adjustment').val() || 0;
    spl_30 = $('#spl_30').val() || 0;
    legal_holiday = $('#legal_holiday').val() || 0;
    
    
    let product;
    let product2
    product = (parseFloat(basic_pay) + parseFloat(late)
                    + parseFloat(absent) + parseFloat(under_time)
                    + parseFloat(normal_working_day_ot) + parseFloat(holiday_ot)
                    + parseFloat(basic_pay_adjustment)
                    + parseFloat(spl_30)
                    + parseFloat(legal_holiday));

    product2 = product.toFixed(2);
    const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    $('#gross_pay').val(stringNumber);
    $('#gross_pay2').val(product2);
    
    }


    // this is for computation of total deduction

$(document).ready(function() {
    $('#sss,#sss_provident,#phic,#hdmf,#other_adjustment').on('input', function() {
        calculatetotalDeduction();
       
    });
    });

    function calculatetotalDeduction() {
    
    let sss;
    let sss_provident;
    let phic;
    let hdmf;
    let other_adjustment;
   
   
   


    sss = $('#sss').val() || 0;
    sss_provident = $('#sss_provident').val() || 0;
    phic = $('#phic').val() || 0;
    hdmf = $('#hdmf').val() || 0;
    other_adjustment =  $('#other_adjustment').val() || 0;
    
    
    
    let product;
    let product2
    product = (parseFloat(sss) + parseFloat(sss_provident)
                    + parseFloat(phic) + parseFloat(hdmf)
                    + parseFloat(other_adjustment)
                    );

    product2 = product.toFixed(2);
    const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    $('#total_deduction').val(stringNumber);
    $('#total_deduction2').val(product2);
   
    }

