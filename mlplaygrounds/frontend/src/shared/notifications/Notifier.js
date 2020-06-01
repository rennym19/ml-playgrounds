import { store } from 'react-notifications-component'

export function notify(title, message, type) {
  store.addNotification({
    title: title,
    message: message,
    type: type,
    insert: 'top',
    container: 'top-center',
    animationIn: ['animated', 'fadeIn'],
    animationOut: ['animated', 'fadeOut'],
    dismiss: {
      duration: 5000,
      showIcon: true
    }
  })
}

export function notifyErrors(errors) {
  if (errors.hasOwnProperty('non_field_errors')) {
    notifyNonFieldErrors(errors)
  } else {
    notifyFieldErrors(errors)
  }
}

function notifyNonFieldErrors(errors) {
  notify('Error', errors.non_field_errors[0], 'danger')
}

function notifyFieldErrors(errors) {
  for (let field in errors)
    notify(field, errors[field][0], 'danger')
}
