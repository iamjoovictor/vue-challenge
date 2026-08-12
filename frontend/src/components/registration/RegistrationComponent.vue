<style lang="scss">
@import '../registration/RegistrationComponent.scss';
</style>

<script lang="ts">
import ToastMessageService from '@/middleware/components/toastMessage.service';
import type { Category } from '@/middleware/inteface/category';
import type { Product } from '@/middleware/inteface/product';
import type { SaleHistoryItem, ProductSaleItem, CategorySaleItem } from '@/middleware/inteface/sale';
import router from '@/router';
import CategoryService from '@/services/category/category.service';
import ProductService from '@/services/product/product.service';
import SaleService from '@/services/sale/sale.service';
import { environment } from '@/environments/environment';

const categoryService = new CategoryService();
const productService = new ProductService();
const saleService = new SaleService();
const toastMessageService = new ToastMessageService();

export default {
    data() {
        return {
            allCategories: [] as Category[],
            allProducts: [] as Product[],
            mapCategories: {} as any,
            dialogCategoryVisible: false as boolean,
            dialogCategoryHeader: '' as string,
            formDialogCategory: {} as Category,
            dialogProductVisible: false as boolean,
            dialogProductHeader: '' as string,
            formDialogProduct: {} as Product,
            isLoading: false as boolean,
            verifyLoadingVariable: { category: false, products: false },
            // sell dialog
            dialogSellVisible: false as boolean,
            formSell: { product_id: null as number | null, quantity: 1 },
            sellProductName: '' as string,
            sellProductStock: 0 as number,
            isSelling: false as boolean,
            // dashboard data
            salesHistory: [] as SaleHistoryItem[],
            topProducts: [] as ProductSaleItem[],
            categorySales: [] as CategorySaleItem[],
            ws: null as any,
        }
    },
    computed: {
        totalStock(): number {
            return this.allProducts.reduce((acc: number, p: Product) => acc + (p.quantity ?? 0), 0);
        },
        totalStockValue(): number {
            return this.allProducts.reduce((acc: number, p: Product) => acc + p.price * (p.quantity ?? 0), 0);
        },
        donutChartData(): any {
            if (!this.categorySales.length) return null;
            const colors = ['#6366f1', '#34d399', '#f59e0b', '#64748b'];
            return {
                labels: this.categorySales.map((c: CategorySaleItem) => c.name),
                datasets: [{ data: this.categorySales.map((c: CategorySaleItem) => c.total), backgroundColor: colors, borderWidth: 0 }],
            };
        },
        donutChartOptions(): any {
            return {
                responsive: true,
                plugins: {
                    legend: { position: 'right', labels: { color: '#94a3b8', font: { size: 12 } } },
                },
            };
        },
        barChartData(): any {
            if (!this.topProducts.length) return null;
            const palette = ['#6366f1','#f87171','#34d399','#f59e0b','#60a5fa','#a78bfa','#fb923c','#ec4899','#22d3ee','#84cc16'];
            return {
                labels: this.topProducts.map((p: ProductSaleItem) => p.name),
                datasets: [{ label: 'Units Sold', data: this.topProducts.map((p: ProductSaleItem) => p.total), backgroundColor: palette, borderRadius: 4 }],
            };
        },
        barChartOptions(): any {
            return {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                    y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                },
            };
        },
    },
    beforeMount() {
        this.isLoading = true;
        this.getAllCategories();
        this.getAllProducts();
        this.loadDashboard();
    },
    mounted() {
        this.connectWebSocket();
    },
    beforeUnmount() {
        if (this.ws) this.ws.close();
    },
    methods: {
        async handleCheckout() {
            localStorage.removeItem('token');
            router.push('/login');
        },

        // WebSocket
        connectWebSocket() {
            const wsUrl = environment.ws + 'websocket/ws/';
            this.ws = new WebSocket(wsUrl);
            this.ws.onmessage = (event: MessageEvent) => {
                try {
                    const data = JSON.parse(event.data);
                    if (data.event === 'sale_created') {
                        this.loadDashboard();
                        this.getAllProducts();
                    }
                } catch {}
            };
        },

        // Dashboard
        async loadDashboard() {
            saleService.getSalesHistory().then(r => { this.salesHistory = r.data; }).catch(() => {});
            saleService.getTopProducts().then(r => { this.topProducts = r.data; }).catch(() => {});
            saleService.getCategorySales().then(r => { this.categorySales = r.data; }).catch(() => {});
        },

        // Sell
        openSellDialog(product: Product) {
            this.formSell = { product_id: Number(product.id), quantity: 1 };
            this.sellProductName = product.name;
            this.sellProductStock = product.quantity ?? 0;
            this.dialogSellVisible = true;
        },
        async handleSell() {
            if (this.formSell.quantity < 1) { toastMessageService.error("Quantity must be at least 1"); return; }
            if (this.formSell.quantity > this.sellProductStock) { toastMessageService.error(`Insufficient stock (${this.sellProductStock} available)`); return; }
            this.isSelling = true;
            this.dialogSellVisible = false;
            saleService.createSale({ product_id: this.formSell.product_id!, quantity: this.formSell.quantity })
                .then(async () => {
                    toastMessageService.sucess(`Sale registered for '${this.sellProductName}'`);
                    this.isSelling = false;
                    await this.getAllProducts();
                    await this.loadDashboard();
                })
                .catch((error: any) => {
                    this.isSelling = false;
                    const detail = error.response?.data?.detail;
                    if (error.response?.status === 400) toastMessageService.error(detail ?? "Insufficient stock");
                    else toastMessageService.error("Server error");
                });
        },

        // Category Service
        async getAllCategories() {
            this.isLoading = true;
            categoryService.getAllCategories()
                .then((response) => {
                    let data: Category[] = response.data;
                    this.mapCategories = {};
                    data.map((value: Category) => { this.mapCategories[Number(value.id)] = value; });
                    this.allCategories = data;
                    this.verifyLoadingVariable.category = true;
                    this.verifyLoading();
                });
        },
        async createCategory() {
            this.isLoading = true;
            categoryService.createCategory(this.formDialogCategory)
                .then(async () => {
                    toastMessageService.sucess(`The category '${this.formDialogCategory.name}' has been created successfully.`);
                    await this.getAllCategories();
                });
        },
        async updateCategory() {
            this.isLoading = true;
            categoryService.updateCategory(this.formDialogCategory)
                .then(async () => {
                    toastMessageService.sucess(`The category '${this.formDialogCategory.name}' has been updated successfully.`);
                    await this.getAllCategories();
                });
        },
        async deleteCategory(category: Category) {
            this.isLoading = true;
            this.dialogCategoryVisible = false;
            categoryService.deleteCategory(Number(category.id))
                .then(async () => {
                    toastMessageService.sucess(`The category '${category.name}' has been successfully deleted.`);
                    await this.getAllCategories();
                });
        },

        // Product Service
        async getAllProducts() {
            this.isLoading = true;
            productService.getAllProducts()
                .then((response) => {
                    let data: Product[] = response.data;
                    this.allProducts = data;
                    this.verifyLoadingVariable.products = true;
                    this.verifyLoading();
                });
        },
        async createProduct() {
            this.isLoading = true;
            productService.createProduct(this.formDialogProduct)
                .then(async () => {
                    toastMessageService.sucess(`The product '${this.formDialogProduct.name}' has been created successfully.`);
                    await this.getAllProducts();
                });
        },
        async updateProduct() {
            this.isLoading = true;
            productService.updateProduct(this.formDialogProduct)
                .then(async () => {
                    toastMessageService.sucess(`The product '${this.formDialogProduct.name}' has been updated successfully.`);
                    await this.getAllProducts();
                });
        },
        async deleteProduct(product: Product) {
            this.isLoading = true;
            this.dialogProductVisible = false;
            productService.deleteProduct(Number(product.id))
                .then(async () => {
                    toastMessageService.sucess(`The product '${product.name}' has been successfully deleted.`);
                    await this.getAllProducts();
                });
        },

        // Dialogs — Category
        async openCategoryDialog(type: string, category: Category) {
            this.dialogCategoryVisible = true;
            if (type === 'add') { this.dialogCategoryHeader = 'Add category'; this.clearCategoryDialog(); }
            else if (type === 'edit') { this.dialogCategoryHeader = 'Edit category'; this.setCategoryDialog(category); }
            else { this.dialogCategoryHeader = 'Delete category'; this.setCategoryDialog(category); }
        },
        clearCategoryDialog() { this.formDialogCategory.id = null; this.formDialogCategory.name = ''; },
        setCategoryDialog(category: Category) { this.formDialogCategory.id = category.id; this.formDialogCategory.name = category.name; },
        async onEnterConfirmCategoryDialog() {
            if (this.formDialogCategory.name.trim()) {
                this.dialogCategoryVisible = false;
                if (this.dialogCategoryHeader === 'Add category') await this.createCategory();
                else await this.updateCategory();
            } else { toastMessageService.error("Fill in all fields"); }
        },

        // Dialogs — Product
        async openProductDialog(type: string, product: Product) {
            this.dialogProductVisible = true;
            if (type === 'add') { this.dialogProductHeader = 'Add product'; this.clearProductDialog(); }
            else if (type === 'edit') { this.dialogProductHeader = 'Edit product'; this.setProductDialog(product); }
            else { this.dialogProductHeader = 'Delete product'; this.setProductDialog(product); }
        },
        clearProductDialog() {
            this.formDialogProduct.id = null;
            this.formDialogProduct.name = '';
            this.formDialogProduct.price = 0;
            this.formDialogProduct.expiration_date = new Date();
            this.formDialogProduct.image = null;
            this.formDialogProduct.id_category = null;
            this.formDialogProduct.quantity = 0;
        },
        setProductDialog(product: Product) {
            this.formDialogProduct.id = product.id;
            this.formDialogProduct.name = product.name;
            this.formDialogProduct.price = product.price;
            this.formDialogProduct.expiration_date = new Date(product.expiration_date);
            this.formDialogProduct.image = product.image;
            this.formDialogProduct.id_category = product.id_category;
            this.formDialogProduct.quantity = product.quantity ?? 0;
            this.formDialogProduct.expiration_date.setDate(this.formDialogProduct.expiration_date.getDate() + 1);
        },
        async onEnterConfirmProductDialog() {
            let dateToFormat = (this.formDialogProduct.expiration_date as Date).toLocaleDateString('pt-BR').split('/');
            this.formDialogProduct.expiration_date = `${dateToFormat[2]}-${dateToFormat[1]}-${dateToFormat[0]}`;
            if (this.formDialogProduct.name.trim() && this.formDialogProduct.id_category != null) {
                this.dialogProductVisible = false;
                if (this.dialogProductHeader === 'Add product') await this.createProduct();
                else await this.updateProduct();
            } else { toastMessageService.error("Fill in all fields"); }
        },

        async verifyLoading() {
            if (this.verifyLoadingVariable.category && this.verifyLoadingVariable.products) {
                this.isLoading = false;
            }
        },

        formatDate(dateStr: string): string {
            const d = new Date(dateStr);
            return d.toLocaleDateString('pt-BR') + ' ' + d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
        },
    }
}
</script>

<template>
    <!-- Loading overlay -->
    <Teleport to="body">
        <div class="dash-overlay" v-if="isLoading">
            <div class="dash-spinner">
                <svg viewBox="0 0 38 38" xmlns="http://www.w3.org/2000/svg" width="40" height="40" stroke="#6366f1">
                    <g fill="none" fill-rule="evenodd">
                        <g transform="translate(1 1)" stroke-width="2">
                            <circle stroke-opacity=".25" cx="18" cy="18" r="18"></circle>
                            <path d="M36 18c0-9.94-8.06-18-18-18">
                                <animateTransform attributeName="transform" type="rotate" from="0 18 18" to="360 18 18"
                                    dur="0.8s" repeatCount="indefinite"></animateTransform>
                            </path>
                        </g>
                    </g>
                </svg>
                <span>Loading…</span>
            </div>
        </div>
    </Teleport>

    <div class="dashboard" :class="{ 'dashboard--loading': isLoading }">
        <!-- Header -->
        <header class="dash-header">
            <div class="dash-brand">
                <i class="pi pi-box"></i>
                <span>Inventory</span>
            </div>
            <button class="dash-logout" @click="handleCheckout()">
                <i class="pi pi-sign-out"></i>
                <span>Logout</span>
            </button>
        </header>

        <!-- Content -->
        <main class="dash-main">
            <div class="dash-inner">
                <Tabs :value="0">
                    <TabList>
                        <Tab :value="0"><i class="pi pi-chart-bar"></i><span>Overview</span></Tab>
                        <Tab :value="1"><i class="pi pi-tags"></i><span>Categories</span></Tab>
                        <Tab :value="2"><i class="pi pi-box"></i><span>Products</span></Tab>
                    </TabList>
                    <TabPanels>

                        <!-- ── Overview ─────────────────────────────────────────── -->
                        <TabPanel :value="0">
                            <!-- KPI cards -->
                            <div class="kpi-row">
                                <div class="kpi-card">
                                    <div class="kpi-icon kpi-icon--purple"><i class="pi pi-box"></i></div>
                                    <div class="kpi-body">
                                        <span class="kpi-value">{{ allProducts.length }}</span>
                                        <span class="kpi-label">Products</span>
                                    </div>
                                </div>
                                <div class="kpi-card">
                                    <div class="kpi-icon kpi-icon--green"><i class="pi pi-tags"></i></div>
                                    <div class="kpi-body">
                                        <span class="kpi-value">{{ allCategories.length }}</span>
                                        <span class="kpi-label">Categories</span>
                                    </div>
                                </div>
                                <div class="kpi-card">
                                    <div class="kpi-icon kpi-icon--blue"><i class="pi pi-warehouse"></i></div>
                                    <div class="kpi-body">
                                        <span class="kpi-value">{{ totalStock }}</span>
                                        <span class="kpi-label">Units in Stock</span>
                                    </div>
                                </div>
                                <div class="kpi-card">
                                    <div class="kpi-icon kpi-icon--yellow"><i class="pi pi-dollar"></i></div>
                                    <div class="kpi-body">
                                        <span class="kpi-value">${{ totalStockValue.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) }}</span>
                                        <span class="kpi-label">Stock Value</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Charts row -->
                            <div class="dash-overview-grid">
                                <!-- Histórico de Vendas -->
                                <div class="dash-card">
                                    <div class="dash-card-header">
                                        <i class="pi pi-history"></i>
                                        <h3>Histórico de Vendas</h3>
                                        <span class="count-badge">last 4</span>
                                    </div>
                                    <div v-if="!salesHistory.length" class="dash-empty">
                                        <i class="pi pi-inbox"></i>
                                        <span>No sales yet</span>
                                    </div>
                                    <table class="history-table" v-else>
                                        <thead>
                                            <tr>
                                                <th>Date / Time</th>
                                                <th>User</th>
                                                <th>Product</th>
                                                <th>Qty</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="sale in salesHistory" :key="sale.id">
                                                <td class="text-muted">{{ formatDate(sale.sold_at) }}</td>
                                                <td>{{ sale.username }}</td>
                                                <td>{{ sale.product_name }}</td>
                                                <td><span class="qty-badge">{{ sale.quantity }}</span></td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>

                                <!-- Vendas por Categoria (donut) -->
                                <div class="dash-card">
                                    <div class="dash-card-header">
                                        <i class="pi pi-chart-pie"></i>
                                        <h3>Vendas por Categoria</h3>
                                    </div>
                                    <div v-if="!donutChartData" class="dash-empty">
                                        <i class="pi pi-inbox"></i>
                                        <span>No sales yet</span>
                                    </div>
                                    <div class="chart-wrap" v-else>
                                        <Chart type="doughnut" :data="donutChartData" :options="donutChartOptions" />
                                    </div>
                                </div>
                            </div>

                            <!-- Produtos mais Vendidos (bar) -->
                            <div class="dash-card dash-card--full">
                                <div class="dash-card-header">
                                    <i class="pi pi-chart-bar"></i>
                                    <h3>Produtos mais Vendidos</h3>
                                    <span class="count-badge">top 10</span>
                                </div>
                                <div v-if="!barChartData" class="dash-empty">
                                    <i class="pi pi-inbox"></i>
                                    <span>No sales yet</span>
                                </div>
                                <div class="chart-wrap chart-wrap--bar" v-else>
                                    <Chart type="bar" :data="barChartData" :options="barChartOptions" />
                                </div>
                            </div>
                        </TabPanel>

                        <!-- ── Categories ───────────────────────────────────────── -->
                        <TabPanel :value="1">
                            <div class="panel-head">
                                <div class="panel-title">
                                    <h2>Categories</h2>
                                    <span class="count-badge">{{ allCategories.length }}</span>
                                </div>
                                <button class="btn-add" @click="openCategoryDialog('add', { id: null, name: '' })">
                                    <i class="pi pi-plus"></i><span>Add Category</span>
                                </button>
                            </div>
                            <DataTable :value="allCategories" tableStyle="min-width: 100%">
                                <Column field="id" header="#" style="width: 80px;"></Column>
                                <Column field="name" header="Name"></Column>
                                <Column field="" header="Actions" style="width: 110px;">
                                    <template #body="category">
                                        <div class="row-actions">
                                            <button class="icon-btn icon-btn--edit" @click="openCategoryDialog('edit', category.data)" title="Edit"><i class="pi pi-pencil"></i></button>
                                            <button class="icon-btn icon-btn--delete" @click="openCategoryDialog('delete', category.data)" title="Delete"><i class="pi pi-trash"></i></button>
                                        </div>
                                    </template>
                                </Column>
                            </DataTable>
                        </TabPanel>

                        <!-- ── Products ─────────────────────────────────────────── -->
                        <TabPanel :value="2">
                            <div class="panel-head">
                                <div class="panel-title">
                                    <h2>Products</h2>
                                    <span class="count-badge">{{ allProducts.length }}</span>
                                </div>
                                <button class="btn-add" @click="openProductDialog('add', { id: null, name: '', price: 0, expiration_date: new Date(), image: null, id_category: null, quantity: 0 })">
                                    <i class="pi pi-plus"></i><span>Add Product</span>
                                </button>
                            </div>
                            <DataTable :value="allProducts" tableStyle="min-width: 100%">
                                <Column field="id" header="#" style="width: 50px;"></Column>
                                <Column field="name" header="Name"></Column>
                                <Column field="price" header="Price" style="width: 110px;">
                                    <template #body="product">
                                        <span class="price-tag">${{ Number(product.data.price).toFixed(2) }}</span>
                                    </template>
                                </Column>
                                <Column field="quantity" header="Stock" style="width: 80px;">
                                    <template #body="product">
                                        <span :class="['stock-badge', product.data.quantity === 0 ? 'stock-badge--empty' : product.data.quantity <= 5 ? 'stock-badge--low' : '']">
                                            {{ product.data.quantity }}
                                        </span>
                                    </template>
                                </Column>
                                <Column field="expiration_date" header="Expires" style="width: 130px;"></Column>
                                <Column field="image" header="Image" style="width: 70px;">
                                    <template #body="product">
                                        <div class="img-cell">
                                            <img v-if="product.data.image" :src="product.data.image" alt="product" />
                                            <span v-else class="img-empty"><i class="pi pi-image"></i></span>
                                        </div>
                                    </template>
                                </Column>
                                <Column field="id_category" header="Category">
                                    <template #body="product">
                                        <span class="cat-tag" v-if="mapCategories[product.data.id_category]">
                                            {{ mapCategories[product.data.id_category].name }}
                                        </span>
                                    </template>
                                </Column>
                                <Column field="" header="Actions" style="width: 150px;">
                                    <template #body="product">
                                        <div class="row-actions">
                                            <button class="icon-btn icon-btn--sell" @click="openSellDialog(product.data)" title="Sell" :disabled="product.data.quantity === 0">
                                                <i class="pi pi-shopping-cart"></i>
                                            </button>
                                            <button class="icon-btn icon-btn--edit" @click="openProductDialog('edit', product.data)" title="Edit"><i class="pi pi-pencil"></i></button>
                                            <button class="icon-btn icon-btn--delete" @click="openProductDialog('delete', product.data)" title="Delete"><i class="pi pi-trash"></i></button>
                                        </div>
                                    </template>
                                </Column>
                            </DataTable>
                        </TabPanel>
                    </TabPanels>
                </Tabs>
            </div>
        </main>
    </div>

    <!-- Dialog: Category -->
    <Dialog v-model:visible="dialogCategoryVisible" modal :header="dialogCategoryHeader" :style="{ width: '26rem' }">
        <template v-if="dialogCategoryHeader !== 'Delete category'">
            <div class="dlg-field">
                <label for="cat-name">Name</label>
                <InputText id="cat-name" autocomplete="off" v-model="formDialogCategory.name" placeholder="Category name" />
            </div>
        </template>
        <template v-else>
            <div class="dlg-confirm">
                <i class="pi pi-exclamation-triangle"></i>
                <p>Delete <strong>{{ formDialogCategory.name }}</strong>? This cannot be undone.</p>
            </div>
        </template>
        <div class="dlg-actions">
            <button class="btn-cancel" @click="dialogCategoryVisible = false">Cancel</button>
            <button class="btn-danger" @click="deleteCategory(formDialogCategory)" v-if="dialogCategoryHeader === 'Delete category'"><i class="pi pi-trash"></i> Delete</button>
            <button class="btn-confirm" @click="onEnterConfirmCategoryDialog()" v-else><i class="pi pi-check"></i> Save</button>
        </div>
    </Dialog>

    <!-- Dialog: Product -->
    <Dialog v-model:visible="dialogProductVisible" modal :header="dialogProductHeader" :style="{ width: '30rem' }">
        <template v-if="dialogProductHeader !== 'Delete product'">
            <div class="dlg-grid">
                <div class="dlg-field">
                    <label for="prod-name">Name</label>
                    <InputText id="prod-name" autocomplete="off" v-model="formDialogProduct.name" placeholder="Product name" />
                </div>
                <div class="dlg-field">
                    <label for="prod-price">Price</label>
                    <InputNumber id="prod-price" v-model="formDialogProduct.price" :min="0" fluid :maxFractionDigits="5" autocomplete="off" placeholder="0.00" />
                </div>
                <div class="dlg-field">
                    <label for="prod-qty">Stock Quantity</label>
                    <InputNumber id="prod-qty" v-model="formDialogProduct.quantity" :min="0" fluid autocomplete="off" placeholder="0" />
                </div>
                <div class="dlg-field">
                    <label>Expiration Date</label>
                    <DatePicker v-model="formDialogProduct.expiration_date" dateFormat="dd/mm/yy" />
                </div>
                <div class="dlg-field">
                    <label for="prod-img">Image URL</label>
                    <InputText id="prod-img" autocomplete="off" v-model="formDialogProduct.image" placeholder="https://…" />
                </div>
                <div class="dlg-field">
                    <label>Category</label>
                    <Select v-model="formDialogProduct.id_category" :options="allCategories" optionLabel="name" placeholder="Select a category" optionValue="id" />
                </div>
            </div>
        </template>
        <template v-else>
            <div class="dlg-confirm">
                <i class="pi pi-exclamation-triangle"></i>
                <p>Delete <strong>{{ formDialogProduct.name }}</strong>? This cannot be undone.</p>
            </div>
        </template>
        <div class="dlg-actions">
            <button class="btn-cancel" @click="dialogProductVisible = false">Cancel</button>
            <button class="btn-danger" @click="deleteProduct(formDialogProduct)" v-if="dialogProductHeader === 'Delete product'"><i class="pi pi-trash"></i> Delete</button>
            <button class="btn-confirm" @click="onEnterConfirmProductDialog()" v-else><i class="pi pi-check"></i> Save</button>
        </div>
    </Dialog>

    <!-- Dialog: Sell -->
    <Dialog v-model:visible="dialogSellVisible" modal header="Register Sale" :style="{ width: '24rem' }">
        <div class="dlg-sell">
            <p class="sell-product-name">{{ sellProductName }}</p>
            <p class="sell-stock-info">Available stock: <strong>{{ sellProductStock }}</strong></p>
            <div class="dlg-field">
                <label for="sell-qty">Quantity to sell</label>
                <InputNumber id="sell-qty" v-model="formSell.quantity" :min="1" :max="sellProductStock" fluid />
            </div>
        </div>
        <div class="dlg-actions">
            <button class="btn-cancel" @click="dialogSellVisible = false">Cancel</button>
            <button class="btn-confirm" @click="handleSell()"><i class="pi pi-shopping-cart"></i> Confirm Sale</button>
        </div>
    </Dialog>
</template>