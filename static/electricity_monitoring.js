
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



