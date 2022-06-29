
function getAddress(zip, street, district, city, state) {

    $(zip).mask('99999-999');
      let formClear = () => {
          // Limpa valores do formulário de cep.
          $(zip).val("");
      }
      //Quando o campo cep perde o foco.
      $(zip).blur(() => {
              let zipCode = $(zip).val().replace(/\D/g, '');

          //Verifica se campo cep possui valor informado.
          if (zipCode != "") {

              //Expressão regular para validar o CEP.
              let validCep = /^[0-9]{8}$/;

              //Valida o formato do CEP.
              if(validCep.test(zipCode)) {

                  //Preenche os campos com "..." enquanto consulta webservice.
                  $(street).val("...");
                  $(district).val("...");
                  $(city).val("...");
                  $(state).val("...");

                  //Consulta o webservice viacep.com.br/
                  $.getJSON(`https://viacep.com.br/ws/${zipCode}/json/?callback=?`, data => {

                      if (!("erro" in data)) {
                          //Atualiza os campos com os valores da consulta.
                          $(street).val(data.logradouro);
                          $(district).val(data.bairro);
                          $(city).val(data.localidade);
                          $(state).val(data.uf);


                      } //end if.
                      else {
                          //CEP pesquisado não foi encontrado.
                          formClear();
                          alert("CEP não encontrado.");
                      }
                  });
              } //end if.
              else {
                  //cep é inválido.
                  formClear();
                  alert("Formato de CEP inválido.");
              }
          } //end if.
          else {
              //cep sem valor, limpa formulário.
              formClear();
          }
      });

};