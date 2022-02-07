<template>
  <q-page 
    class="flex"
  >
    <div
      class="full-width"
    >
      <q-card
        style="max-width: 500px; margin: 50px auto;"
      >
        <q-form
          @submit="onSubmit"
          @reset="onReset"
          class="q-gutter-md"
        >
          <q-card-section>
            <div class="text-h6">
              Watering configuration
            </div>
          </q-card-section>
          <q-separator />
          <q-card-section>
            <q-select 
              outlined 
              v-model="cms2" 
              :options="options" 
              dense 
              label="water (cms2)"
              color="dark"
            >
              <template v-slot:prepend>
                <q-icon name="mdi-water"></q-icon>
              </template>
            </q-select>
            <q-checkbox v-model='enabled' label="Enabled" color="dark"></q-checkbox>
          </q-card-section>
          <q-card-section>
            <q-btn label="Save" type="submit" color="secondary"/>
            <q-btn label="Reset" type="reset" color="secondary" flat class="q-ml-sm" />
          </q-card-section>
        </q-form>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";
import { api } from 'boot/axios';

export default defineComponent({
  name: "PageConfigurations",
  data () {
    return {
      cms2: ref(null),
      enabled: ref(null),
      options: [
        '100', '200', '300'
      ]
    }

  },
  methods: {
    onSubmit() {
      let currentObj = this;

      let postData = {
        cms2: currentObj.cms2,
        enabled: currentObj.enabled,
      }

      api.post('/configuration', postData)
      .then((response) => {
        let data = response.data
        currentObj.cms2 = data.cms2
        currentObj.enabled = data.enabled == true

        this.$q.notify({
          message: 'saved',
          icon: 'mdi-check',
          color: 'positive',
          position: 'top'
        })
      })
      .catch(() => {
        this.$q.notify({
          color: 'negative',
          icon: 'mdi-alert-circle',
          message: 'failed',
          position: 'top'
        })
      })
    },
    onReset() {
      let currentObj = this;

      api.get('/configuration')
      .then((response) => {
        let data = response.data
        currentObj.cms2 = data.cms2
        currentObj.enabled = data.enabled == true
      })
      .catch(() => {
      })
    }
  },
  created () {
    this.onReset()
  }
});
</script>
