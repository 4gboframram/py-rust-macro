# __use_macros__('rust_macro.builtins')


py_gte!(
    "3.8.10",
    compile_error!("oof")
)