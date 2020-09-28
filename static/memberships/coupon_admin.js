
django.jQuery("#id_duration").change(function (){
  if (django.jQuery("#id_duration").val() == 1)
      {
      django.jQuery(".field-duration_months").show(0);
      }
  else
      {
      django.jQuery(".field-duration_months").hide(0);
      }
  console.log(django.jQuery("#id_duration").val())
})