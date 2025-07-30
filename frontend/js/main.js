document.addEventListener('DOMContentLoaded', () => {
    // --- Configuração e Variáveis ---
    const API_URL = 'http://newtremed.pythonanywhere.com';
    const token = localStorage.getItem('accessToken');
    
    // Elementos da Página
    const searchInput = document.getElementById('search-input');
    const brandFilter = document.getElementById('brand-filter');
    const supplierFilter = document.getElementById('supplier-filter');
    const minPriceFilter = document.getElementById('min-price-filter');
    const maxPriceFilter = document.getElementById('max-price-filter');
    const tableBody = document.getElementById('results-table-body');
    const loadingIndicator = document.getElementById('loading-indicator');
    const resultsCount = document.getElementById('results-count');
    const logoutButton = document.getElementById('logout-button');

    // --- 1. Segurança: Proteção da Página ---
    if (!token) {
        // Se não houver token, redireciona para a página de login
        window.location.href = 'login.html';
        return; // Para a execução do script
    }

    // --- 2. Função Principal de Busca ---
    const fetchProducts = async () => {
        loadingIndicator.classList.remove('d-none');
        tableBody.innerHTML = ''; // Limpa resultados antigos
        resultsCount.textContent = '';

        const searchTerm = searchInput.value;

        // Só faz a busca se o termo tiver 3 ou mais letras, ou se um filtro estiver ativo
        if (searchTerm.length < 3 && !brandFilter.value && !supplierFilter.value && !minPriceFilter.value && !maxPriceFilter.value) {
            loadingIndicator.classList.add('d-none');
            resultsCount.textContent = 'Digite pelo menos 3 letras para iniciar a busca.';
            return;
        }

        // Constrói a URL da API com os filtros
        const params = new URLSearchParams();
        if (searchTerm.length >= 3) params.append('q', searchTerm);
        if (brandFilter.value) params.append('brand', brandFilter.value);
        if (supplierFilter.value) params.append('supplier', supplierFilter.value);
        if (minPriceFilter.value) params.append('min_price', minPriceFilter.value);
        if (maxPriceFilter.value) params.append('max_price', maxPriceFilter.value);
        params.append('limit', 200); // Limite de resultados por busca

        try {
            const response = await fetch(`${API_URL}/api/products/search?${params.toString()}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!response.ok) {
                // Se o token for inválido/expirado, desloga o utilizador
                if (response.status === 401) {
                    localStorage.removeItem('accessToken');
                    window.location.href = 'login.html';
                }
                throw new Error('Falha na busca de produtos.');
            }

            const products = await response.json();
            renderTable(products);

        } catch (error) {
            console.error('Erro:', error);
            resultsCount.textContent = 'Erro ao carregar dados.';
        } finally {
            loadingIndicator.classList.add('d-none');
        }
    };

    // --- 3. Função para Renderizar a Tabela ---
    const renderTable = (products) => {
        if (products.length === 0) {
            resultsCount.textContent = 'Nenhum resultado encontrado.';
            return;
        }
        
        products.forEach(product => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${product.produto || ''}</td>
                <td>${product.cod_fornecedor || ''}</td>
                <td>${product.anvisa || ''}</td>
                <td>R$ ${product.preco_unitario_venda ? product.preco_unitario_venda.toFixed(2) : '0.00'}</td>
                <td>${product.marca || ''}</td>
                <td>${product.fornecedor || ''}</td>
                <td>
                    ${product.observacao ? `<a href="${product.observacao}" class="catalog-link" target="_blank">Ver</a>` : ''}
                </td>
                <td>${product.data_de_atualizacao ? new Date(product.data_de_atualizacao).toLocaleDateString() : ''}</td>
            `;
            tableBody.appendChild(tr);
        });
        resultsCount.textContent = `${products.length} resultados encontrados.`;
    };

    // --- 4. Funções para Carregar os Filtros ---
    const populateFilter = async (filterElement, endpoint) => {
        try {
            const response = await fetch(`${API_URL}${endpoint}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await response.json();
            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item;
                option.textContent = item;
                filterElement.appendChild(option);
            });
        } catch (error) {
            console.error(`Erro ao carregar filtro ${endpoint}:`, error);
        }
    };

    // --- 5. Configuração dos Eventos ---
    let searchTimeout;
    const DEBOUNCE_DELAY = 300; // Atraso de 300ms após o utilizador parar de digitar

    const triggerSearch = () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(fetchProducts, DEBOUNCE_DELAY);
    };

    searchInput.addEventListener('keyup', triggerSearch);
    brandFilter.addEventListener('change', fetchProducts);
    supplierFilter.addEventListener('change', fetchProducts);
    minPriceFilter.addEventListener('change', triggerSearch);
    maxPriceFilter.addEventListener('change', triggerSearch);

    logoutButton.addEventListener('click', () => {
        localStorage.removeItem('accessToken');
        window.location.href = 'login.html';
    });
    
    // --- 6. Inicialização da Página ---
    // Carrega os filtros de marca e fornecedor assim que a página abre
    populateFilter(brandFilter, '/api/filters/brands');
    populateFilter(supplierFilter, '/api/filters/suppliers');
    // Faz uma busca inicial (opcional)
    fetchProducts();
});