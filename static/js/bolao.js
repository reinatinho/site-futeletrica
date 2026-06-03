document.addEventListener('DOMContentLoaded', function() {
    initPalpites();
    initExtrasSelects();
    initSalvar();
    loadExistingData();
});

function focusProximoInput(atual) {
    const allInputs = Array.from(document.querySelectorAll('.placar-input:not([disabled])'));
    const idx = allInputs.indexOf(atual);
    if (idx > -1 && idx < allInputs.length - 1) {
        const proximo = allInputs[idx + 1];
        proximo.focus();
        proximo.select();
    }
}

function initPalpites() {
    const inputs = document.querySelectorAll('.placar-input');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            let val = this.value.replace(/[^0-9]/g, '');
            if (val.length > 1) val = val.charAt(0);
            if (parseInt(val) > 9) val = '9';
            this.value = val;

            if (val !== '') {
                this.classList.add('filled');
            } else {
                this.classList.remove('filled');
            }

            const grupo = this.closest('.jogo-row').dataset.grupo;
            updateClassificacao(grupo);
            updateGrupoStatus(grupo);

            // Ao digitar um dígito (0-9), pula automaticamente para o próximo campo
            if (val !== '') {
                focusProximoInput(this);
            }
        });

        input.addEventListener('keydown', function(e) {
            if (e.key === 'Tab' || e.key === 'Enter') {
                e.preventDefault();
                focusProximoInput(this);
            }
        });

        input.addEventListener('focus', function() {
            this.select();
        });
    });
}

function initExtrasSelects() {
    const selects = document.querySelectorAll('.extra-select');
    const sorted = [...TODAS_SELECOES].sort((a, b) => a.nome.localeCompare(b.nome));
    selects.forEach(select => {
        sorted.forEach(sel => {
            const option = document.createElement('option');
            option.value = sel.id;
            option.textContent = sel.nome;
            option.dataset.codigo = sel.codigo ? sel.codigo.toLowerCase() : '';
            select.appendChild(option);
        });

        // Wrap select in custom dropdown with flag images
        wrapSelectWithFlags(select);
    });
}

function wrapSelectWithFlags(select) {
    const wrapper = document.createElement('div');
    wrapper.className = 'custom-select-wrapper';

    const display = document.createElement('div');
    display.className = 'custom-select-display';
    display.innerHTML = '<span class="csd-placeholder">Selecione...</span>';

    const dropdown = document.createElement('div');
    dropdown.className = 'custom-select-dropdown';

    const search = document.createElement('input');
    search.type = 'text';
    search.className = 'custom-select-search';
    search.placeholder = 'Buscar seleção...';
    dropdown.appendChild(search);

    const itemsBox = document.createElement('div');
    itemsBox.className = 'custom-select-items';
    dropdown.appendChild(itemsBox);

    const sorted = [...TODAS_SELECOES].sort((a, b) => a.nome.localeCompare(b.nome));
    sorted.forEach(sel => {
        const item = document.createElement('div');
        item.className = 'custom-select-item';
        item.dataset.value = sel.id;
        item.dataset.nome = sel.nome.toLowerCase();
        const cod = sel.codigo ? sel.codigo.toLowerCase() : '';
        item.innerHTML = `<img src="/static/images/flags/${cod}.png" class="csd-flag" alt="${cod}"> ${sel.nome}`;
        item.addEventListener('click', () => {
            select.value = sel.id;
            select.dispatchEvent(new Event('change'));
            display.innerHTML = `<img src="/static/images/flags/${cod}.png" class="csd-flag" alt="${cod}"> ${sel.nome}`;
            dropdown.classList.remove('open');
            wrapper.classList.remove('open');
        });
        itemsBox.appendChild(item);
    });

    search.addEventListener('input', function() {
        const termo = this.value.toLowerCase().trim();
        itemsBox.querySelectorAll('.custom-select-item').forEach(it => {
            it.style.display = it.dataset.nome.includes(termo) ? '' : 'none';
        });
    });
    search.addEventListener('click', e => e.stopPropagation());

    display.addEventListener('click', (e) => {
        e.stopPropagation();
        document.querySelectorAll('.custom-select-wrapper.open').forEach(w => {
            if (w !== wrapper) { w.classList.remove('open'); w.querySelector('.custom-select-dropdown').classList.remove('open'); }
        });
        const willOpen = !dropdown.classList.contains('open');
        dropdown.classList.toggle('open');
        wrapper.classList.toggle('open');
        if (willOpen) { search.value = ''; search.dispatchEvent(new Event('input')); setTimeout(() => search.focus(), 50); }
    });

    document.addEventListener('click', () => {
        dropdown.classList.remove('open');
        wrapper.classList.remove('open');
    });

    select.style.display = 'none';
    select.parentElement.appendChild(wrapper);
    wrapper.appendChild(display);
    wrapper.appendChild(dropdown);

    // If already has a value, show it
    if (select.value) {
        const sel = sorted.find(s => s.id == select.value);
        if (sel) {
            const cod = sel.codigo ? sel.codigo.toLowerCase() : '';
            display.innerHTML = `<img src="/static/images/flags/${cod}.png" class="csd-flag" alt="${cod}"> ${sel.nome}`;
        }
    }
}

function loadExistingData() {
    // Palpites de jogos
    for (const [jogoId, dados] of Object.entries(PALPITES_EXISTENTES)) {
        const row = document.querySelector(`.jogo-row[data-jogo-id="${jogoId}"]`);
        if (row) {
            const casaInput = row.querySelector('.gols-casa');
            const foraInput = row.querySelector('.gols-fora');
            if (dados.gols_casa !== null) {
                casaInput.value = dados.gols_casa;
                casaInput.classList.add('filled');
            }
            if (dados.gols_fora !== null) {
                foraInput.value = dados.gols_fora;
                foraInput.classList.add('filled');
            }
        }
    }

    // Extras
    for (const [tipo, selecaoId] of Object.entries(EXTRAS_EXISTENTES)) {
        const select = document.querySelector(`.extra-select[data-tipo="${tipo}"]`);
        if (select && selecaoId) {
            select.value = selecaoId;
            // Update custom dropdown display
            const wrapper = select.parentElement.querySelector('.custom-select-wrapper');
            if (wrapper) {
                const display = wrapper.querySelector('.custom-select-display');
                const sel = TODAS_SELECOES.find(s => s.id == selecaoId);
                if (sel && display) {
                    const cod = sel.codigo ? sel.codigo.toLowerCase() : '';
                    display.innerHTML = `<img src="/static/images/flags/${cod}.png" class="csd-flag" alt="${cod}"> ${sel.nome}`;
                }
            }
        }
    }

    // Calcular classificações de todos os grupos
    const grupos = new Set();
    document.querySelectorAll('.jogo-row').forEach(row => {
        grupos.add(row.dataset.grupo);
    });
    grupos.forEach(grupo => {
        updateClassificacao(grupo);
        updateGrupoStatus(grupo);
    });

    // Palpites de classificação existentes (1º ao 4º por grupo).
    // Se já houver palpite salvo, marca o grupo como "manual" para não sobrescrever.
    for (const [grupoId, posicoes] of Object.entries(CLASSIFICACOES_EXISTENTES)) {
        let algum = false;
        for (const [posicao, selecaoId] of Object.entries(posicoes)) {
            const select = document.querySelector(`.classif-select[data-grupo="${grupoId}"][data-posicao="${posicao}"]`);
            if (select && selecaoId) {
                select.value = selecaoId;
                algum = true;
            }
        }
        if (algum) {
            const box = document.querySelector(`.meu-palpite-classif[data-grupo-id="${grupoId}"]`);
            if (box) box.dataset.manual = '1';
        }
    }

    initClassifSelects();
}

function initClassifSelects() {
    // Impede que a mesma seleção seja escolhida em mais de uma posição do grupo
    document.querySelectorAll('.meu-palpite-classif').forEach(box => {
        const selects = box.querySelectorAll('.classif-select');
        function atualizarOpcoes() {
            const escolhidos = Array.from(selects).map(s => s.value).filter(v => v);
            selects.forEach(sel => {
                Array.from(sel.options).forEach(opt => {
                    if (!opt.value) return;
                    opt.disabled = escolhidos.includes(opt.value) && sel.value !== opt.value;
                });
            });
        }
        box._refreshOpcoes = atualizarOpcoes;
        selects.forEach(sel => sel.addEventListener('change', function() {
            // Ajuste manual do usuário: para de preencher automaticamente
            box.dataset.manual = '1';
            atualizarOpcoes();
        }));
        atualizarOpcoes();
    });
}

function updateClassificacao(grupoLetra) {
    const grupoCard = document.getElementById(`grupo-${grupoLetra}`);
    if (!grupoCard) return;

    const jogos = grupoCard.querySelectorAll('.jogo-row');
    const tabela = grupoCard.querySelector('.tabela-classificacao tbody');
    if (!tabela) return;

    const rows = tabela.querySelectorAll('tr');
    const stats = {};

    rows.forEach(row => {
        const selId = row.dataset.selecaoId;
        stats[selId] = { id: selId, pts: 0, v: 0, e: 0, d: 0, gp: 0, gc: 0, sg: 0 };
    });

    jogos.forEach(jogo => {
        const casaInput = jogo.querySelector('.gols-casa');
        const foraInput = jogo.querySelector('.gols-fora');
        const golsCasa = casaInput.value !== '' ? parseInt(casaInput.value) : null;
        const golsFora = foraInput.value !== '' ? parseInt(foraInput.value) : null;

        if (golsCasa === null || golsFora === null) return;

        const idCasa = jogo.dataset.casaId;
        const idFora = jogo.dataset.foraId;

        if (!idCasa || !idFora || !stats[idCasa] || !stats[idFora]) return;

        stats[idCasa].gp += golsCasa;
        stats[idCasa].gc += golsFora;
        stats[idFora].gp += golsFora;
        stats[idFora].gc += golsCasa;

        if (golsCasa > golsFora) {
            stats[idCasa].v += 1;
            stats[idCasa].pts += 3;
            stats[idFora].d += 1;
        } else if (golsCasa < golsFora) {
            stats[idFora].v += 1;
            stats[idFora].pts += 3;
            stats[idCasa].d += 1;
        } else {
            stats[idCasa].e += 1;
            stats[idCasa].pts += 1;
            stats[idFora].e += 1;
            stats[idFora].pts += 1;
        }
    });

    // Saldo de gols
    Object.values(stats).forEach(s => { s.sg = s.gp - s.gc; });

    // Ordenar
    const sorted = Object.values(stats).sort((a, b) => {
        if (b.pts !== a.pts) return b.pts - a.pts;
        if (b.sg !== a.sg) return b.sg - a.sg;
        if (b.gp !== a.gp) return b.gp - a.gp;
        return 0;
    });

    // Atualizar tabela (apenas simulação visual, não define o palpite)
    sorted.forEach((s, idx) => {
        const row = tabela.querySelector(`tr[data-selecao-id="${s.id}"]`);
        if (!row) return;

        row.querySelector('.pos').textContent = idx + 1;
        row.querySelector('.pts').textContent = s.pts;
        row.querySelector('.vit').textContent = s.v;
        row.querySelector('.emp').textContent = s.e;
        row.querySelector('.der').textContent = s.d;
        row.querySelector('.gp').textContent = s.gp;
        row.querySelector('.gc').textContent = s.gc;
        row.querySelector('.sg').textContent = s.sg;

        // Reordenar visualmente
        tabela.appendChild(row);
    });

    // Auto-preencher o palpite de classificação com a ordem simulada
    // (somente quando o grupo está completo e o usuário ainda não ajustou manualmente)
    const box = grupoCard.querySelector('.meu-palpite-classif');
    if (box && box.dataset.manual !== '1') {
        const inputs = grupoCard.querySelectorAll('.placar-input');
        const allFilled = inputs.length > 0 && Array.from(inputs).every(i => i.value !== '');
        if (allFilled) {
            sorted.forEach((s, idx) => {
                const sel = box.querySelector(`.classif-select[data-posicao="${idx + 1}"]`);
                if (sel) sel.value = s.id;
            });
            if (typeof box._refreshOpcoes === 'function') box._refreshOpcoes();
        }
    }
}

function updateGrupoStatus(grupoLetra) {
    const grupoCard = document.getElementById(`grupo-${grupoLetra}`);
    if (!grupoCard) return;

    const inputs = grupoCard.querySelectorAll('.placar-input');
    const total = inputs.length;
    const filled = Array.from(inputs).filter(i => i.value !== '').length;

    const statusEl = grupoCard.querySelector('.grupo-status');
    if (filled === total) {
        statusEl.innerHTML = '<i class="fas fa-check-circle"></i> Completo';
        statusEl.classList.add('completo');
    } else {
        statusEl.innerHTML = `<i class="fas fa-circle"></i> ${filled}/${total}`;
        statusEl.classList.remove('completo');
    }
}

function initSalvar() {
    const btnRascunho = document.getElementById('btn-rascunho');
    const btnEnviar = document.getElementById('btn-enviar');

    // Carregar rascunho local ao iniciar (se não tem dados do servidor)
    loadRascunho();

    if (btnRascunho) {
        btnRascunho.addEventListener('click', function() {
            salvarRascunhoLocal();
            showToast('Rascunho salvo no seu navegador!', 'success');
        });
    }

    if (btnEnviar) {
        btnEnviar.addEventListener('click', async function() {
            const validation = validateAll();
            const avisoEl = document.getElementById('validacao-aviso');
            const textoEl = document.getElementById('validacao-texto');

            if (!validation.valid) {
                avisoEl.style.display = 'block';
                textoEl.textContent = validation.message;
                avisoEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                return;
            }

            avisoEl.style.display = 'none';
            btnEnviar.disabled = true;
            btnEnviar.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';

            const data = collectData();

            try {
                const response = await fetch(SALVAR_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': CSRF_TOKEN,
                    },
                    body: JSON.stringify(data),
                });

                const result = await response.json();

                if (response.ok && result.success) {
                    showToast('Palpites enviados com sucesso!', 'success');
                    limparRascunhoLocal();
                } else {
                    showToast(result.error || 'Erro ao enviar', 'error');
                }
            } catch (err) {
                showToast('Erro de conexão. Tente novamente.', 'error');
            }

            btnEnviar.disabled = false;
            btnEnviar.innerHTML = '<i class="fas fa-paper-plane"></i> Enviar Palpites';
        });
    }
}

function salvarRascunhoLocal() {
    const data = collectDataParcial();
    localStorage.setItem('bolao_rascunho', JSON.stringify(data));
    localStorage.setItem('bolao_rascunho_data', new Date().toLocaleString('pt-BR'));
    updateRascunhoInfo();
}

function loadRascunho() {
    const saved = localStorage.getItem('bolao_rascunho');
    if (!saved) return;

    // Só carrega rascunho se não tem dados do servidor
    const temDadosServidor = Object.keys(PALPITES_EXISTENTES).length > 0;
    if (temDadosServidor) return;

    try {
        const data = JSON.parse(saved);
        if (data.palpites) {
            for (const [jogoId, valores] of Object.entries(data.palpites)) {
                const row = document.querySelector(`.jogo-row[data-jogo-id="${jogoId}"]`);
                if (row) {
                    const casaInput = row.querySelector('.gols-casa');
                    const foraInput = row.querySelector('.gols-fora');
                    if (valores.gols_casa !== undefined && casaInput) {
                        casaInput.value = valores.gols_casa;
                        casaInput.classList.add('filled');
                    }
                    if (valores.gols_fora !== undefined && foraInput) {
                        foraInput.value = valores.gols_fora;
                        foraInput.classList.add('filled');
                    }
                }
            }
        }
        if (data.extras) {
            for (const [tipo, selecaoId] of Object.entries(data.extras)) {
                const select = document.querySelector(`.extra-select[data-tipo="${tipo}"]`);
                if (select && selecaoId) {
                    select.value = selecaoId;
                    const wrapper = select.parentElement.querySelector('.custom-select-wrapper');
                    if (wrapper) {
                        const display = wrapper.querySelector('.custom-select-display');
                        const sel = TODAS_SELECOES.find(s => s.id == selecaoId);
                        if (sel && display) {
                            const cod = sel.codigo ? sel.codigo.toLowerCase() : '';
                            display.innerHTML = `<img src="/static/images/flags/${cod}.png" class="csd-flag" alt="${cod}"> ${sel.nome}`;
                        }
                    }
                }
            }
        }
        if (data.classificacoes) {
            for (const [grupoId, posicoes] of Object.entries(data.classificacoes)) {
                let algum = false;
                for (const [posicao, selecaoId] of Object.entries(posicoes)) {
                    const select = document.querySelector(`.classif-select[data-grupo="${grupoId}"][data-posicao="${posicao}"]`);
                    if (select && selecaoId) { select.value = selecaoId; algum = true; }
                }
                if (algum) {
                    const box = document.querySelector(`.meu-palpite-classif[data-grupo-id="${grupoId}"]`);
                    if (box) box.dataset.manual = '1';
                }
            }
            initClassifSelects();
        }
        updateRascunhoInfo();
    } catch (e) {}
}

function collectDataParcial() {
    const palpites = {};
    const extras = {};

    document.querySelectorAll('#etapa-grupos-content .jogo-row:not(.jogo-row-elim)').forEach(row => {
        const jogoId = row.dataset.jogoId;
        const casa = row.querySelector('.gols-casa');
        const fora = row.querySelector('.gols-fora');
        if (casa && fora && (casa.value !== '' || fora.value !== '')) {
            palpites[jogoId] = {};
            if (casa.value !== '') palpites[jogoId].gols_casa = parseInt(casa.value);
            if (fora.value !== '') palpites[jogoId].gols_fora = parseInt(fora.value);
        }
    });

    document.querySelectorAll('.extra-select').forEach(select => {
        if (select.value) {
            extras[select.dataset.tipo] = parseInt(select.value);
        }
    });

    const classificacoes = {};
    document.querySelectorAll('.meu-palpite-classif').forEach(box => {
        const grupoId = box.dataset.grupoId;
        box.querySelectorAll('.classif-select').forEach(sel => {
            if (sel.value) {
                if (!classificacoes[grupoId]) classificacoes[grupoId] = {};
                classificacoes[grupoId][sel.dataset.posicao] = parseInt(sel.value);
            }
        });
    });

    return { palpites, extras, classificacoes };
}

function limparRascunhoLocal() {
    localStorage.removeItem('bolao_rascunho');
    localStorage.removeItem('bolao_rascunho_data');
    updateRascunhoInfo();
}

function updateRascunhoInfo() {
    const infoEl = document.getElementById('rascunho-info');
    if (!infoEl) return;
    const dataStr = localStorage.getItem('bolao_rascunho_data');
    if (dataStr) {
        infoEl.style.display = 'block';
        infoEl.textContent = `Rascunho local salvo em: ${dataStr}`;
    } else {
        infoEl.style.display = 'none';
    }
}

function validateAll() {
    const jogosRows = document.querySelectorAll('#etapa-grupos-content .jogo-row:not(.jogo-row-elim)');
    const vazios = [];

    jogosRows.forEach(row => {
        const casa = row.querySelector('.gols-casa');
        const fora = row.querySelector('.gols-fora');
        if (!casa || !fora || casa.value === '' || fora.value === '') {
            const grupo = row.dataset.grupo;
            const times = row.querySelector('.time-casa .time-nome').textContent.trim() +
                         ' x ' + row.querySelector('.time-fora .time-nome').textContent.trim();
            vazios.push(`Grupo ${grupo}: ${times}`);
        }
    });

    // Check extras
    const extras = document.querySelectorAll('.extra-select');
    const extrasVazios = [];
    extras.forEach(select => {
        if (!select.value) {
            extrasVazios.push(select.dataset.tipo);
        }
    });

    if (vazios.length > 0) {
        const msg = `${vazios.length} jogo(s) sem palpite. Preencha todos para salvar.`;
        return { valid: false, message: msg };
    }

    // Classificação: todas as 4 posições de cada grupo devem estar preenchidas
    const gruposIncompletos = [];
    document.querySelectorAll('.meu-palpite-classif').forEach(box => {
        const selects = box.querySelectorAll('.classif-select');
        const preenchidos = Array.from(selects).filter(s => s.value).length;
        if (preenchidos < selects.length) {
            const titulo = box.closest('.grupo-card')?.querySelector('.grupo-header h3')?.textContent.trim() || 'Grupo';
            gruposIncompletos.push(titulo);
        }
    });
    if (gruposIncompletos.length > 0) {
        return { valid: false, message: `Defina a classificação (1º ao 4º) de: ${gruposIncompletos.join(', ')}.` };
    }

    if (extrasVazios.length > 0) {
        return { valid: false, message: `Selecione todos os palpites especiais (campeão, vice, 3º, pior).` };
    }

    return { valid: true };
}

function collectData() {
    const palpites = {};
    const classificacoes = {};
    const extras = {};

    // Palpites de jogos (somente fase de grupos)
    document.querySelectorAll('#etapa-grupos-content .jogo-row:not(.jogo-row-elim)').forEach(row => {
        const jogoId = row.dataset.jogoId;
        const casa = row.querySelector('.gols-casa').value;
        const fora = row.querySelector('.gols-fora').value;
        if (casa !== '' && fora !== '') {
            palpites[jogoId] = {
                gols_casa: parseInt(casa),
                gols_fora: parseInt(fora),
            };
        }
    });

    // Classificações: posições 1º a 4º escolhidas manualmente em cada grupo
    document.querySelectorAll('.meu-palpite-classif').forEach(box => {
        const grupoId = box.dataset.grupoId;
        if (!grupoId) return;
        box.querySelectorAll('.classif-select').forEach(sel => {
            if (sel.value) {
                if (!classificacoes[grupoId]) classificacoes[grupoId] = {};
                classificacoes[grupoId][sel.dataset.posicao] = parseInt(sel.value);
            }
        });
    });

    // Extras
    document.querySelectorAll('.extra-select').forEach(select => {
        if (select.value) {
            extras[select.dataset.tipo] = parseInt(select.value);
        }
    });

    return { palpites, classificacoes, extras };
}

function showToast(message, type) {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i> ${message}`;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}
