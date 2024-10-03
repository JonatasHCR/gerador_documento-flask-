// Função para adicionar novos campos de input
function adicionarCampo() {
    const container = document.getElementById("input-container");
    
    // Cria um novo div para os campos Nome e Email
    const div = document.createElement("div");

    // Adiciona o campo Nome
    div.innerHTML = `
    <div class="row">
            <label for="staticEmail" class="col-sm-2 col-form-label">Variavel: </label>
            <div class="col">
            <input type="text" required class="form-control" name="variavel" placeholder="Nome da Variavel" aria-label="Nome da Variavel">
            </div>
            <div class="col">
            <input type="text" required class="form-control" name="ref_variavel" placeholder="Referencia da Variavel" aria-label="Referencia da Variavel">
            </div>
            <div class="col">
                <input type="text" class="form-control" name="default_variavel"  placeholder="Valor Padrão da Variavel" aria-label="Valor Padrão da Variavel">
            </div>
            <div class="col">
            <button type="button" class="btn btn-danger" onclick="removerCampo(this)">Remover</button>
             </div>
          </div>
    `;
    
    // Adiciona o div ao container
    container.appendChild(div);
}

// Função para remover campos de input
function removerCampo(botao) {
    const div = botao.parentElement;
    div.parentElement.remove();
}