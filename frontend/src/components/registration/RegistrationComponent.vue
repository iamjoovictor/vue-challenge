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
    <div class="loading" v-if="isLoading">
        <svg viewBox="0 0 38 38" xmlns="http://www.w3.org/2000/svg" width="128" height="128" stroke="#007bff">
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
    </div>
    <div class="registration-wrapper" :style="{ opacity: isLoading ? 0.3 : 1 }">
        <div class="registration-container">
            <Tabs :value="0">
                <TabList>
                    <Tab :key="'Category'" :value="0">
                        <i class="pi pi-bars">
                            Category
                        </i>
                    </Tab>
                    <Tab :key="'Products'" :value="1">
                        <i class="pi pi-cart-minus">
                            Products
                        </i>

                    </Tab>
                    <Tab :key="'exit'" :value="2" @click="handleCheckout()">
                        <i class="pi pi-sign-out">
                        </i>
                    </Tab>
                </TabList>
                <TabPanels>
                    <!-- TabPanel Category -->
                    <TabPanel :key="'Category'" :value="0">
                        <div class="align-add-button">
                            <button class="pi pi-plus" @click="openCategoryDialog('add', { id: null, name: '' })">
                            </button>
                        </div>
                        <DataTable :value="allCategories" tableStyle="min-width: 100%">
                            <Column :key="'id'" :field="'id'" :header="'Id'" style="width: 25%;">
                            </Column>

                            <Column :key="'name'" :field="'name'" :header="'Name'" style="width: 50%;">
                            </Column>

                            <Column :key="''" :field="''" :header="''" style="width: 25%;">
                                <template #body="category">
                                    <i class="pi pi-pencil" @click="openCategoryDialog('edit', category.data)"></i>
                                    <i class="pi pi-trash" @click="openCategoryDialog('delete', category.data)"></i>
                                </template>
                            </Column>
                        </DataTable>
                    </TabPanel>

                    <!-- TabPanel Product -->
                    <TabPanel :key="'Products'" :value="1">
                        <div class="align-add-button">
                            <button class="pi pi-plus"
                                @click="openProductDialog('add', { id: null, name: '', price: 0, expiration_date: new Date(), image: null, id_category: null })">
                            </button>
                        </div>
                        <DataTable :value="allProducts" tableStyle="min-width: 100%">
                            <Column :key="'id'" :field="'id'" :header="'Id'" style="width: 10%;">
                            </Column>

                            <Column :key="'name'" :field="'name'" :header="'Name'" style="width: 15%;">
                            </Column>

                            <Column :key="'price'" :field="'price'" :header="'Price'" style="width: 15%;">
                            </Column>

                            <Column :key="'expiration_date'" :field="'expiration_date'" :header="'Expiration Date'"
                                style="width: 15%;">
                            </Column>

                            <Column :key="'image'" :field="'image'" :header="'Image'" style="width: 15%;">
                                <template #body="product">
                                    <img v-if="product.data.image" :src="product.data.image" alt="product-image">
                                    {{ product.data.image ? '' : 'No image' }}
                                </template>
                            </Column>

                            <Column :key="'id_category'" :field="'id_category'" :header="'Category'"
                                style="width: 15%;">
                                <template #body="product">
                                    {{ mapCategories[product.data.id_category].name }}
                                </template>
                            </Column>

                            <Column :key="''" :field="''" :header="''" style="width: 15%;">
                                <template #body="product">
                                    <i class="pi pi-pencil" @click="openProductDialog('edit', product.data)"></i>
                                    <i class="pi pi-trash" @click="openProductDialog('delete', product.data)"></i>
                                </template>
                            </Column>
                        </DataTable>
                    </TabPanel>
                </TabPanels>
            </Tabs>
        </div>

        <!-- Dialog Category -->
        <Dialog v-model:visible="dialogCategoryVisible" modal :header="dialogCategoryHeader"
            :style="{ width: '50rem' }">
            <template v-if="dialogCategoryHeader != 'Delete category'">
                <div class="container-input">
                    <label for="name" class="font-semibold w-24">Name</label>
                    <InputText id="name" class="flex-auto" autocomplete="off" v-model="formDialogCategory.name" />
                </div>
            </template>

            <div class="buttons-align">
                <div class="buttons-content">
                    <Button type="button" label="Cancel" severity="secondary"
                        @click="dialogCategoryVisible = false"></Button>
                    <Button type="button" label="Delete" @click="deleteCategory(formDialogCategory)"
                        v-if="dialogCategoryHeader == 'Delete category'"></Button>
                    <Button type="button" label="Save" @click="onEnterConfirmCategoryDialog()" v-else></Button>
                </div>
            </div>
        </Dialog>

        <!-- Dialog Product -->
        <Dialog v-model:visible="dialogProductVisible" modal :header="dialogProductHeader" :style="{ width: '50rem' }">
            <template v-if="dialogProductHeader != 'Delete product'">
                <div class="container-input">
                    <label for="name" class="font-semibold w-24">Name</label>
                    <InputText id="name" class="flex-auto" autocomplete="off" v-model="formDialogProduct.name" />
                </div>

                <div class="container-input">
                    <label for="price" class="font-semibold w-24">Price</label>
                    <InputNumber id="price" v-model="formDialogProduct.price" :min="0" fluid :maxFractionDigits="5"
                        autocomplete="off" />
                </div>

                <div class="container-input">
                    <label for="expiration_date" class="font-semibold w-24">Expiration Date</label>
                    <DatePicker v-model="formDialogProduct.expiration_date" dateFormat="dd/mm/yy" />
                </div>

                <div class="container-input">
                    <label for="image" class="font-semibold w-24">Image Link</label>
                    <InputText id="image" class="flex-auto" autocomplete="off" v-model="formDialogProduct.image" />
                </div>

                <div class="container-input">
                    <label for="category" class="font-semibold w-24">Category</label>
                    <Select v-model="formDialogProduct.id_category" :options="allCategories" optionLabel="name"
                        placeholder="Select a Category" optionValue="id" />
                </div>
            </template>

            <div class="buttons-align">
                <div class="buttons-content">
                    <Button type="button" label="Cancel" severity="secondary"
                        @click="dialogProductVisible = false"></Button>
                    <Button type="button" label="Delete" @click="deleteProduct(formDialogProduct)"
                        v-if="dialogProductHeader == 'Delete product'"></Button>
                    <Button type="button" label="Save" @click="onEnterConfirmProductDialog()" v-else></Button>
                </div>
            </div>
        </Dialog>
    </div>
</template>