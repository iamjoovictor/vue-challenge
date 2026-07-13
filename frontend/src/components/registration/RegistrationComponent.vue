<style lang="scss">
@import '../registration/RegistrationComponent.scss';
</style>

<script lang="ts">
import ToastMessageService from '@/middleware/components/toastMessage.service';
import type { Category } from '@/middleware/inteface/category';
import type { Product } from '@/middleware/inteface/product';
import router from '@/router';
import CategoryService from '@/services/category/category.service';
import ProductService from '@/services/product/product.service';

const categoryService = new CategoryService();
const productService = new ProductService();
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
            verifyLoadingVariable: { category: false, products: false }
        }
    },
    beforeMount() {
        this.isLoading = true;

        this.getAllCategories();
        this.getAllProducts();
    },
    methods: {
        async handleCheckout() {
            setTimeout(() => {
                router.push('/login');
            }, 100);
        },
        // Category Service
        async getAllCategories() {
            this.isLoading = true;

            categoryService.getAllCategories()
                .then((response) => {
                    let data: Category[] = response.data;

                    this.mapCategories = {};

                    data.map((value: Category, index: number) => {
                        this.mapCategories[Number(value.id)] = value
                    })

                    this.allCategories = data;

                    this.verifyLoadingVariable.category = true;
                    this.verifyLoading();
                })
        },
        async createCategory() {
            this.isLoading = true;

            categoryService.createCategory(this.formDialogCategory)
                .then(async (response) => {
                    toastMessageService.sucess(`The category '${this.formDialogCategory.name}' has been created successfully.`);

                    await this.getAllCategories();
                })
        },
        async updateCategory() {
            this.isLoading = true;

            categoryService.updateCategory(this.formDialogCategory)
                .then(async (response) => {
                    toastMessageService.sucess(`The category '${this.formDialogCategory.name}' has been updated successfully.`);

                    await this.getAllCategories();
                })
        },
        async deleteCategory(category: Category) {
            this.isLoading = true;
            this.dialogCategoryVisible = false;

            categoryService.deleteCategory(Number(category.id))
                .then(async (response) => {
                    toastMessageService.sucess(`The category '${category.name}' has been successfully deleted.`);

                    await this.getAllCategories();
                })
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
                })
        },
        async createProduct() {
            this.isLoading = true;

            productService.createProduct(this.formDialogProduct)
                .then(async (response) => {
                    toastMessageService.sucess(`The product '${this.formDialogCategory.name}' has been created successfully.`);

                    await this.getAllProducts();
                })
        },
        async updateProduct() {
            this.isLoading = true;

            productService.updateProduct(this.formDialogProduct)
                .then(async (response) => {
                    toastMessageService.sucess(`The product '${this.formDialogCategory.name}' has been updated successfully.`);

                    await this.getAllProducts();
                })
        },
        async deleteProduct(product: Product) {
            this.isLoading = true;
            this.dialogProductVisible = false;

            productService.deleteProduct(Number(product.id))
                .then(async (response) => {
                    toastMessageService.sucess(`The product '${product.name}' has been successfully deleted.`);

                    await this.getAllProducts();
                })
        },
        // Dialog Category
        async openCategoryDialog(type: string, category: Category) {
            this.dialogCategoryVisible = true;

            if (type == 'add') {
                this.dialogCategoryHeader = 'Add category';
                this.clearCategoryDialog();
            }

            else if (type == 'edit') {
                this.dialogCategoryHeader = 'Edit category';
                this.setCategoryDialog(category);
            }

            else {
                this.dialogCategoryHeader = 'Delete category';
                this.setCategoryDialog(category);
            }
        },
        clearCategoryDialog() {
            this.formDialogCategory.id = null;
            this.formDialogCategory.name = '';
        },
        setCategoryDialog(category: Category) {
            this.formDialogCategory.id = category.id;
            this.formDialogCategory.name = category.name;
        },
        async onEnterConfirmCategoryDialog() {
            if (this.formDialogCategory.name.trim()) {
                this.dialogCategoryVisible = false;

                if (this.dialogCategoryHeader == 'Add category') {
                    await this.createCategory();
                }

                else {
                    await this.updateCategory();
                }

            }

            else {
                toastMessageService.error("Fill in all fields");
            }
        },
        // Dialog Product
        async openProductDialog(type: string, product: Product) {
            this.dialogProductVisible = true;

            if (type == 'add') {
                this.dialogProductHeader = 'Add product';
                this.clearProductDialog();
            }

            else if (type == 'edit') {
                this.dialogProductHeader = 'Edit product';
                this.setProductDialog(product);
            }

            else {
                this.dialogProductHeader = 'Delete product';
                this.setProductDialog(product);
            }
        },
        clearProductDialog() {
            this.formDialogProduct.id = null;
            this.formDialogProduct.name = '';
            this.formDialogProduct.price = 0;
            this.formDialogProduct.expiration_date = new Date();
            this.formDialogProduct.image = null;
            this.formDialogProduct.id_category = null;
        },
        setProductDialog(product: Product) {
            this.formDialogProduct.id = product.id;
            this.formDialogProduct.name = product.name;
            this.formDialogProduct.price = product.price;
            this.formDialogProduct.expiration_date = new Date(product.expiration_date);
            this.formDialogProduct.image = product.image;
            this.formDialogProduct.id_category = product.id_category;

            this.formDialogProduct.expiration_date.setDate(this.formDialogProduct.expiration_date.getDate() + 1);
        },
        async onEnterConfirmProductDialog() {
            let dateToFormat = (this.formDialogProduct.expiration_date as Date).toLocaleDateString('pt-BR').split('/');
            this.formDialogProduct.expiration_date = `${dateToFormat[2]}-${dateToFormat[1]}-${dateToFormat[0]}`;

            if (this.formDialogProduct.name.trim() && this.formDialogProduct.id_category != null) {
                this.dialogProductVisible = false;

                if (this.dialogProductHeader == 'Add product') {
                    await this.createProduct();
                }

                else {
                    await this.updateProduct();
                }
            }

            else {
                toastMessageService.error("Fill in all fields");
            }
        },
        async verifyLoading() {
            if (this.verifyLoadingVariable.category && this.verifyLoadingVariable.products) {
                this.isLoading = false;
            }
        }
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
                        <Tab :key="'Category'" :value="0">
                            <i class="pi pi-tags"></i>
                            <span>Categories</span>
                        </Tab>
                        <Tab :key="'Products'" :value="1">
                            <i class="pi pi-box"></i>
                            <span>Products</span>
                        </Tab>
                    </TabList>
                    <TabPanels>
                        <!-- Categories -->
                        <TabPanel :key="'Category'" :value="0">
                            <div class="panel-head">
                                <div class="panel-title">
                                    <h2>Categories</h2>
                                    <span class="count-badge">{{ allCategories.length }}</span>
                                </div>
                                <button class="btn-add" @click="openCategoryDialog('add', { id: null, name: '' })">
                                    <i class="pi pi-plus"></i>
                                    <span>Add Category</span>
                                </button>
                            </div>
                            <DataTable :value="allCategories" tableStyle="min-width: 100%">
                                <Column field="id" header="#" style="width: 80px;"></Column>
                                <Column field="name" header="Name"></Column>
                                <Column field="" header="Actions" style="width: 110px;">
                                    <template #body="category">
                                        <div class="row-actions">
                                            <button class="icon-btn icon-btn--edit"
                                                @click="openCategoryDialog('edit', category.data)" title="Edit">
                                                <i class="pi pi-pencil"></i>
                                            </button>
                                            <button class="icon-btn icon-btn--delete"
                                                @click="openCategoryDialog('delete', category.data)" title="Delete">
                                                <i class="pi pi-trash"></i>
                                            </button>
                                        </div>
                                    </template>
                                </Column>
                            </DataTable>
                        </TabPanel>

                        <!-- Products -->
                        <TabPanel :key="'Products'" :value="1">
                            <div class="panel-head">
                                <div class="panel-title">
                                    <h2>Products</h2>
                                    <span class="count-badge">{{ allProducts.length }}</span>
                                </div>
                                <button class="btn-add"
                                    @click="openProductDialog('add', { id: null, name: '', price: 0, expiration_date: new Date(), image: null, id_category: null })">
                                    <i class="pi pi-plus"></i>
                                    <span>Add Product</span>
                                </button>
                            </div>
                            <DataTable :value="allProducts" tableStyle="min-width: 100%">
                                <Column field="id" header="#" style="width: 60px;"></Column>
                                <Column field="name" header="Name"></Column>
                                <Column field="price" header="Price" style="width: 120px;">
                                    <template #body="product">
                                        <span class="price-tag">${{ Number(product.data.price).toFixed(2) }}</span>
                                    </template>
                                </Column>
                                <Column field="expiration_date" header="Expires" style="width: 140px;"></Column>
                                <Column field="image" header="Image" style="width: 80px;">
                                    <template #body="product">
                                        <div class="img-cell">
                                            <img v-if="product.data.image" :src="product.data.image" alt="product" />
                                            <span v-else class="img-empty"><i class="pi pi-image"></i></span>
                                        </div>
                                    </template>
                                </Column>
                                <Column field="id_category" header="Category">
                                    <template #body="product">
                                        <span class="cat-tag"
                                            v-if="mapCategories[product.data.id_category]">
                                            {{ mapCategories[product.data.id_category].name }}
                                        </span>
                                    </template>
                                </Column>
                                <Column field="" header="Actions" style="width: 110px;">
                                    <template #body="product">
                                        <div class="row-actions">
                                            <button class="icon-btn icon-btn--edit"
                                                @click="openProductDialog('edit', product.data)" title="Edit">
                                                <i class="pi pi-pencil"></i>
                                            </button>
                                            <button class="icon-btn icon-btn--delete"
                                                @click="openProductDialog('delete', product.data)" title="Delete">
                                                <i class="pi pi-trash"></i>
                                            </button>
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
                <InputText id="cat-name" autocomplete="off" v-model="formDialogCategory.name"
                    placeholder="Category name" />
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
            <button class="btn-danger" @click="deleteCategory(formDialogCategory)"
                v-if="dialogCategoryHeader === 'Delete category'">
                <i class="pi pi-trash"></i> Delete
            </button>
            <button class="btn-confirm" @click="onEnterConfirmCategoryDialog()" v-else>
                <i class="pi pi-check"></i> Save
            </button>
        </div>
    </Dialog>

    <!-- Dialog: Product -->
    <Dialog v-model:visible="dialogProductVisible" modal :header="dialogProductHeader" :style="{ width: '30rem' }">
        <template v-if="dialogProductHeader !== 'Delete product'">
            <div class="dlg-grid">
                <div class="dlg-field">
                    <label for="prod-name">Name</label>
                    <InputText id="prod-name" autocomplete="off" v-model="formDialogProduct.name"
                        placeholder="Product name" />
                </div>
                <div class="dlg-field">
                    <label for="prod-price">Price</label>
                    <InputNumber id="prod-price" v-model="formDialogProduct.price" :min="0" fluid
                        :maxFractionDigits="5" autocomplete="off" placeholder="0.00" />
                </div>
                <div class="dlg-field">
                    <label>Expiration Date</label>
                    <DatePicker v-model="formDialogProduct.expiration_date" dateFormat="dd/mm/yy" />
                </div>
                <div class="dlg-field">
                    <label for="prod-img">Image URL</label>
                    <InputText id="prod-img" autocomplete="off" v-model="formDialogProduct.image"
                        placeholder="https://…" />
                </div>
                <div class="dlg-field">
                    <label>Category</label>
                    <Select v-model="formDialogProduct.id_category" :options="allCategories" optionLabel="name"
                        placeholder="Select a category" optionValue="id" />
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
            <button class="btn-danger" @click="deleteProduct(formDialogProduct)"
                v-if="dialogProductHeader === 'Delete product'">
                <i class="pi pi-trash"></i> Delete
            </button>
            <button class="btn-confirm" @click="onEnterConfirmProductDialog()" v-else>
                <i class="pi pi-check"></i> Save
            </button>
        </div>
    </Dialog>
</template>