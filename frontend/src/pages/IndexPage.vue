<template>
  <q-page class="q-pa-md">
    <div class="text-h4 q-mb-md">Управление товарами</div>
    
    <!-- Форма добавления товара -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="text-h6">Добавить новый товар</div>
        <q-form @submit="addItem" class="q-gutter-md">
          <q-input v-model="newItem.name" label="Наименование" required />
          <q-input v-model.number="newItem.price" type="number" label="Цена" required />
          <q-btn type="submit" color="primary" label="Добавить" />
        </q-form>
      </q-card-section>
    </q-card>

    <!-- Таблица товаров -->
    <q-card>
      <q-card-section>
        <div class="text-h6">Список товаров</div>
        <q-table
          :rows="items"
          :columns="columns"
          row-key="id"
          :loading="loading"
        >
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <q-btn 
                @click="editItem(props.row)" 
                icon="edit" 
                color="blue" 
                flat 
                dense
              />
              <q-btn 
                @click="deleteItem(props.row.id)" 
                icon="delete" 
                color="red" 
                flat 
                dense
              />
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <!-- Диалог редактирования -->
    <q-dialog v-model="editDialog">
      <q-card style="min-width: 300px">
        <q-card-section>
          <div class="text-h6">Редактировать товар</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveEdit" class="q-gutter-md">
            <q-input v-model="editedItem.name" label="Наименование" required />
            <q-input v-model.number="editedItem.price" type="number" label="Цена" required />
            <div class="row justify-end q-gutter-sm">
              <q-btn label="Отмена" v-close-popup />
              <q-btn type="submit" color="primary" label="Сохранить" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const items = ref([])
const loading = ref(false)
const editDialog = ref(false)

const newItem = ref({
  name: '',
  price: 0
})

const editedItem = ref({
  id: null,
  name: '',
  price: 0
})

const columns = [
  { name: 'id', label: 'ID', field: 'id', align: 'left' },
  { name: 'name', label: 'Наименование', field: 'name', align: 'left' },
  { name: 'price', label: 'Цена', field: 'price', align: 'left' },
  { name: 'actions', label: 'Действия', align: 'center' }
]

// Загрузка товаров
const fetchItems = async () => {
  try {
    loading.value = true
    const response = await axios.get('/api/items/')
    items.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке товаров:', error)
  } finally {
    loading.value = false
  }
}

// Добавление товара
const addItem = async () => {
  try {
    await axios.post('/api/items/', newItem.value)
    newItem.value = { name: '', price: 0 }
    await fetchItems()
  } catch (error) {
    console.error('Ошибка при добавлении товара:', error)
  }
}

// Редактирование товара
const editItem = (item) => {
  editedItem.value = { ...item }
  editDialog.value = true
}

// Сохранение изменений
const saveEdit = async () => {
  try {
    await axios.put(`/api/items/${editedItem.value.id}/`, editedItem.value)
    editDialog.value = false
    await fetchItems()
  } catch (error) {
    console.error('Ошибка при сохранении изменений:', error)
  }
}

// Удаление товара
const deleteItem = async (id) => {
  try {
    await axios.delete(`/api/items/${id}/`)
    await fetchItems()
  } catch (error) {
    console.error('Ошибка при удалении товара:', error)
  }
}

// Загружаем товары при загрузке компонента
onMounted(() => {
  fetchItems()
})
</script>
