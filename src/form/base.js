import React from 'react'
import _ from 'lodash'
import { Field, reduxForm, reducer as formReducer } from 'redux-form'
import Ajv from 'ajv'
import ajvLocalize from './locales'
import { StoreWrap, app } from '../index'
import { convert as schemaConvert } from './schema'
import { objectBuilder, fieldBuilder } from './builder'

const ajv = new Ajv({ allErrors: true, v5: true, verbose: true })

const BaseForm = (props) => {
  const { fields, render, option, component, handleSubmit, ...formProps } = props
  const build_fields = objectBuilder(fields, render, { ...option, ...formProps })
  if(component) {
    const FormComponent = component
    return <FormComponent {...props} >{build_fields}</FormComponent>
  } else {
    return (
      <form className="form-horizontal" onSubmit={handleSubmit}>{build_fields}</form>
    )
  }
}

const validateByFields = (errors, values, fields) => {
  fields.forEach(field => {
    if(_.isFunction(field.validate)) {
      const name = field.name
      const err = field.validate(_.get(values, field.name) || null, values)
      if(_.isArray(err)) {
        errors[name] = [ ...(errors[name] || []), ...err ]
      } else if(err) {
        errors[name] = [ ...(errors[name] || []), err ]
      }
    }
  })
  return errors
}

const Form = (props) => {
  const { formKey, validate, fields } = props
  const WrapForm = reduxForm({ 
    form: formKey,
    validate: (values) => {
      let errors = validate ? validate(values) : {}
      return validateByFields(errors, values, fields)
    }
  })(BaseForm)
  return <WrapForm {...props}/>
}

const SchemaForm = (props) => {
  const { formKey, schema } = props
  const ajValidate = ajv.compile(schema)
  const fields = schemaConvert(schema).fields
  
  const WrapForm = reduxForm({ 
    form: formKey,
    validate: (values) => {
      const valid = ajValidate(values)
      if(!valid) {
        const { i18n } = app.context
        if(ajvLocalize[i18n.language]) {
          ajvLocalize[i18n.language](ajValidate.errors)
        }
      }
      let errors = valid ? {} : ajValidate.errors.reduce((prev, err) => {
        if(err.dataPath.length > 1) {
          prev[err.dataPath.substr(1)] = err.message
        } else if(err.dataPath == '' && err.keyword == 'required') {
          prev[err.params.missingProperty] = err.message
        }
        return prev
      }, {})
      errors = validateByFields(errors, values, fields)
      return errors
    }
  })(BaseForm)
  return <WrapForm fields={fields} {...props}/>
}

const FormWrap = StoreWrap({
  contextTypes: {
    _reduxForm: React.PropTypes.object.isRequired
  },
  getState: (context) => {
    const { store, _reduxForm } = context
    return { form: _reduxForm, formState: _reduxForm.getFormState(store.getState()) }
  }
})

export default {
  BaseForm,
  Form,
  SchemaForm,
  FormWrap,
  fieldBuilder,
  objectBuilder,
  schemaConvert
}