import { defineStore } from 'pinia'

export const useContactsStore = defineStore('contacts', {
    state: () => ({
      
        contacts: [],
        selectedContact: null,
    }),
    actions: {

    }
})

