$(document).ready(function(){
    $('#btn_search').click(function(){
        var datefrom = $('#datefrom').val();
        var dateto = $('#dateto').val();

        $.ajax({
            type: 'POST',
            url: '/graphql', // Change this to your GraphQL endpoint
            contentType: 'application/json',
            data: JSON.stringify({
                query: `query MyQuery {
                    getMonthlyPayrollReportTest(datefrom: "${datefrom}", dateto: "${dateto}") {
                        name
                        book
                        totalGrossPay
                        netPay
                        allowance
                        AllowanceMeals
                        developmental
                        allowanceDeduction
                    }
                }`
            }),
            success: function(response) {
                var data = response.data.getMonthlyPayrollReportTest;
                var tbody = $('#table_payroll_monthly_report2');
                tbody.empty();
                console.log(data);
                $.each(data, function(index, item){
                    var row = $('<tr>');
                    row.append($('<td>').text(item.name));
                    row.append($('<td>').text(item.book));
                  
                    row.append($('<td>').text(formatNumber(item.totalGrossPay)));
                    row.append($('<td>').text(formatNumber(item.netPay)));
                    row.append($('<td>').text(formatNumber(item.allowance)));
                    row.append($('<td>').text(formatNumber(item.AllowanceMeals)));
                    row.append($('<td>').text(formatNumber(item.developmental)));
                    row.append($('<td>').text(formatNumber(item.allowanceDeduction)));
                    tbody.append(row);
                });
                initializeDataTable();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});

const initializeDataTable = () => {
    $('#table_payroll_monthly_report').DataTable();
};


function formatNumber(number) {
    // Check if the number is valid
    if (isNaN(number)) {
        return number; // Return as is if not a valid numbergit add 
    }
    
    // Format number with thousand separator and 2 decimal places
    return parseFloat(number).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function payrollListExcel(type){
    var data = document.getElementById('table_payroll_monthly_report2');
    var file = XLSX.utils.table_to_book(data,{sheet: "sheet1"});
    XLSX.write(file,{ booktype: type, bookSST: true, type: 'base64'});
    XLSX.writeFile(file, 'payroll_list.' + type);

}
