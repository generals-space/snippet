#!/bin/bash

source $(cd $(dirname $0) && pwd)/logger.sh

log_info "默认日志等级为 INFO"
log_debug "这是一条 DEBUG 日志" ## 不显示
log_info "这是一条 INFO 日志"
log_warn "这是一条 WARN 日志"
log_error "这是一条 ERROR 日志"
log_success "这是一条 SUCCESS 信息"

log_info "修改日志等级为 DEBUG"
__LOGGER_LOG_LEVEL__=$__LOGGER_LEVEL_DEBUG__
log_debug "这是一条 DEBUG 日志" ## 此时会显示

log_fatal "这是一条 FATAL 日志"
log_info "无法打印这一条日志, 因为FATAL已经让脚本退出"
