$(document).ready(function(){
    $('#fuel_mode').change(function(){
        var fuelMode = $(this).val();
        var vehicleOptions = {
            "Electric": ["EV101", "EV102"],
            "CNG": ["CNG101", "CNG102"],
            "Petrol": ["Petrol101", "Petrol102"],
            "Ethanol": ["Ethanol101", "Ethanol102"],
            "Diesel": ["Diesel101", "Diesel102"]
        };
        var options = vehicleOptions[fuelMode] || ["Please select fuel mode"];
        $('#vehicle').empty();
        $.each(options, function(index, value){
            $('#vehicle').append($('<option>', { value: value, text: value }));
        });
    });
});
