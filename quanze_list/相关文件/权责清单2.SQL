/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2020/7/21 9:12:35                            */
/*==============================================================*/


drop table if exists GOV_DEPT_DUTY_REL;

drop table if exists GOV_DEPT_ITEM_REL;

drop table if exists GOV_DEPT_LIST;

drop table if exists GOV_DUTY_LIST;

drop table if exists GOV_ITEMS_TYPE_DEF;

drop table if exists GOV_ITEM_LIST;

drop table if exists GOV_QUERY_ANSWER;

drop table if exists GOV_SERVICES_FLOW;

drop table if exists GOV_SERVICES_LIST;

drop table if exists GOV_SERVICES_MATERIAL;

drop table if exists GOV_SERVIES_FEE;

/*==============================================================*/
/* Table: GOV_DEPT_DUTY_REL                                     */
/*==============================================================*/
create table GOV_DEPT_DUTY_REL
(
   REL_ID               char(256), comment '关系ID',
   DEPT_CODE            char(256), comment '部门机构代码',
   DUTY_CODE            char(256), comment '事项编码',
   CREATE_USER          char(50),  comment '创建人',
   CREATE_TIME          timestamp, comment '创建时间',
   UPDATE_USER          char(50),  comment '最后更新人',
   UPDATE_TIME          timestamp  comment '最后更新时间',
);

alter table GOV_DEPT_DUTY_REL comment '部门与责任关系';

/*==============================================================*/
/* Table: GOV_DEPT_ITEM_REL                                     */
/*==============================================================*/
create table GOV_DEPT_ITEM_REL
(
   REL_ID               char(256), comment '关系ID',
   DEPT_CODE            char(200), comment '部门机构代码',
   ITEM_CODE            char(256), comment '事项编码',
   CREATE_USER          char(50),  comment '创建人',
   CREATE_TIME          timestamp, comment '创建时间',
   UPDATE_USER          char(50),  comment '最后更新人',
   UPDATE_TIME          timestamp  comment '最后更新时间',
);

alter table GOV_DEPT_ITEM_REL comment '部门与事项关系表';

/*==============================================================*/
/* Table: GOV_DEPT_LIST                                         */
/*==============================================================*/
create table GOV_DEPT_LIST
(
   DEPT_CODE            char(50),  comment '部门机构编码',
   DEPT_NAME            char(200), comment '部门名称',
   UP_DEPT_CODE         char(50),  comment '上级部门机构编码',
   UP_DEPT_NAME         char(200), comment '上级部门机构名称',
   CREATE_USER          char(50),  comment '创建人',
   CREATE_TIME          timestamp, comment '创建时间',
   UPDATE_USER          char(50),  comment '最后更新人',
   UPDATE_TIME          timestamp  comment '最后更新时间',
);

alter table GOV_DEPT_LIST comment '行政部门清单';

/*==============================================================*/
/* Table: GOV_DUTY_LIST                                         */
/*==============================================================*/
create table GOV_DUTY_LIST
(
   DUTY_CODE            char(50),  comment '责任编码',
   DUTY_NAME            char(100), comment '责任名称',
   "ITEM_TYPE-code"     char(50),  comment '事项类别编码',
   DUTY_SCOPE           longtext(40000), comment '责任边界',
   DEPT_DUTY_DESC       longtext(40000), comment '部门职责',
   PUNISH_DESC          longtext(40000), comment '追责情形',
   NO_PUNISH_DESC       longtext(40000), comment '免责情形',
   JASON_CONTENT        longtext(100000), comment '采集到的责任事项的JASON串的全部内容',
   CREATE_USER          char(50),   comment '创建人',
   CREATE_TIME          timestamp,  comment '创建时间',
   UPDATE_USER          char(50),   comment '最后更新人',
   UPDATE_TIME          timestamp   comment '最后更新时间',
);

alter table GOV_DUTY_LIST comment '责任清单';

/*==============================================================*/
/* Table: GOV_ITEMS_TYPE_DEF                                    */
/*==============================================================*/
create table GOV_ITEMS_TYPE_DEF
(
   ITEM_TYPE_CODE       char(50) comment '事项类别编码',
   ITEM_TYPE_NAME       char(100) comment '事项类别名称',
   ITEM_TYPE_DESC       char(1000) comment '事项类别说明',
   CREATE_USER          char(50),   comment '创建人',
   CREATE_TIME          timestamp,  comment '创建时间',
   UPDATE_USER          char(50),   comment '最后更新人',
   UPDATE_TIME          timestamp   comment '最后更新时间',
);

alter table GOV_ITEMS_TYPE_DEF comment '权力事项类别定义';

/*==============================================================*/
/* Table: GOV_ITEM_LIST                                         */
/*==============================================================*/
create table GOV_ITEM_LIST
(
   ITEM_CODE            char(50) comment '事项编码',
   ITEM_NAME            char(100) comment '事项名称',
   ITEM_TYPE_CODE       char(50) comment '事项类别编码',
   OWNER_DEPT_CODE      char(50) comment '实施主体',
   ADMIN_LEVEL          int comment '行驶层级1:省 2：市 3：区',
   IS_MOVEIN            char(50), comment '是否已进驻',
   ITEM_DESC            longtext(40000) comment '实施依据',  //Right_依据
   REMARKS              longtext(40000) comment '事项说明',  //Right_说明
   JASON_CONTENT        longtext(100000), comment '采集到的事项的JASON串的全部内容',
   CREATE_USER          char(50),   comment '创建人',
   CREATE_TIME          timestamp,  comment '创建时间',
   UPDATE_USER          char(50),   comment '最后更新人',
   UPDATE_TIME          timestamp   comment '最后更新时间',
);

alter table GOV_ITEM_LIST comment '事项清单';

/*==============================================================*/
/* Table: GOV_QUERY_ANSWER                                      */
/*==============================================================*/
create table GOV_QUERY_ANSWER
(
   QA_ID                int,          comment '问题ID',
   SERVICES_CODE        char(50),     comment '服务业务编码',
   QUERY_DESC           char(4000),   comment '问题',
   ANSWER_DESC          longtext(40000),   comment '答案',
   CREATE_USER          char(50),     comment '创建人',
   CREATE_TIME          timestamp,    comment '创建时间',
   UPDATE_USER          char(50),     comment '最后更新人',
   UPDATE_TIME          timestamp     comment '最后更新时间',
);

alter table GOV_QUERY_ANSWER comment '常见问题';

/*==============================================================*/
/* Table: GOV_SERVICES_FLOW                                     */
/*==============================================================*/
create table GOV_SERVICES_FLOW
(
   FLOW_ID              int comment '流程ID',
   SERVICES_CODE        char(50) comment '服务业务编码',
   STEP_NO              char(2) comment '流程环节序号',
   STEP_NAME            char(100), comment '流程环节名称',
   STEP_LIMIT           char(10),  comment '流程环节时限',
   STEP_PASS_STD        longtext(40000), comment '审批标准', # tips+content 融合
   AUDIT_ORG            char(200),  comment '审批机构', # 审批人
   CREATE_USER          char(50),   comment '创建人',
   CREATE_TIME          timestamp,   comment '创建时间',
   UPDATE_USER          char(50),   comment '最后更新人',
   UPDATE_TIME          timestamp   comment '最后更新时间',
);

alter table GOV_SERVICES_FLOW comment '服务业务流程';

/*==============================================================*/
/* Table: GOV_SERVICES_LIST                                     */
/*==============================================================*/
create table GOV_SERVICES_LIST
(
   SERVICES_CODE        char(50) comment '业务编码',
   SERVICES_NAME        char(100) comment '业务名称',
   ITEM_CODE            char(50) comment '所属事项编码',
   LEGAL_LIMIT          char(10) comment '法定办结时限',  ## 数值单位说明
   LEGAL_LIMIT_UNIT     char(10) comment '法定办结时限单位',
   LEGAL_LIMIT_DESC     char(1000) comment '法定办结时限说明',
   PROMISE_LIMIT        char(10)   comment '承诺办结时限',
   PROMISE_LIMIT_UNIT   char(10),  comment '承诺办结时限单位',
   PROMISE_LIMIT_DESC   char(1000),comment '承诺办结时限说明',
   SERVICE_OBJECTS      char(1000),comment '承诺办结时限说明', ## 服务对象
   "ACC_ CRIT"          longtext(40000), comment '受理标准', ## 受理套件
   OBJECT_TYPE          char(10),  comment '办件类型',
   WORK_TYPE            char(100), comment '办理形式',
   WORKPLACE_TIMES      char(10),  comment '到办事现场次数',
   OTHERS               char(1000), comment '特殊程序', ## 无则不处理，有则json串
   WORK_ADDRESS         char(1000), comment '办理地点', ## 窗口办理
   WORK_TIME            char(200),  comment '办理时间',
   ASK_TYPE             char(200),  comment '咨询方式', ## json串
   COMPLAIN_TYPE        char(500),  comment '监督投诉方式',
   ONLINE_DESC          char(1000), comment '网上办理深度',
   SCOPE                char(2000), comment '通办范围',
   REL_DEPT_CODE        char(200),  comment '联办机构',
   ITEM_EDITION         char(20),   comment '事项版本',
   CREATE_USER          char(50),   comment '创建人', 
   CREATE_TIME          timestamp,  comment '创建时间',
   UPDATE_USER          char(50),   comment '最后更新人',
   UPDATE_TIME          timestamp   comment '最后更新时间',
);

alter table GOV_SERVICES_LIST comment '服务业务清单';

/*==============================================================*/
/* Table: GOV_SERVICES_MATERIAL                                 */
/*==============================================================*/
create table GOV_SERVICES_MATERIAL  ### 申请材料
(
   MATERIAL_ID          int,        comment '材料ID',
   "SERVICES-code"      char(50),   comment '服务业务编码',
   MATERIAL_NAME        char(100),  comment '材料名称',
   SUBMIT_TYPE          char(50),   comment '提供形式',## 固定值
   MATERIAL_TYPE        char(50),   comment '材料类型',## 纸质/电子
   MATERIAL_SRC         char(50),   comment '来源渠道',
   PAPER_NUM            char(50),   comment '纸质材料份数',
   PAPER_SIZE           char(100),   comment '纸质材料规格', ## A4
   NECESSARY            char(100),   comment '材料必要性',
   WRITE_NOTE           char(2000),  comment '填报须知',
   SAMPLE_URL           char(1000),  comment '填报实例模板路径',
   PROVIDE_REASON       longtext(40000),  comment '要求提供材料依据', ## 有的有
   REMARKS              char(4000)   comment '说明',## 来源渠道说明
   CREATE_USER          char(50),   comment '创建人', 
   CREATE_TIME          timestamp,  comment '创建时间',
   UPDATE_USER          char(50),   comment '最后更新人',
   UPDATE_TIME          timestamp   comment '最后更新时间',
);

alter table GOV_SERVICES_MATERIAL comment '服务业务材料清单';

/*==============================================================*/
/* Table: GOV_SERVIES_FEE                                       */
/*==============================================================*/
create table GOV_SERVIES_FEE
(
   FEE_CODE                char(256), comment '收费项编码',
   FEE_NAME                char(256), comment '收费项名称',
   SERVICES_CODE               char(256),comment '服务业务编码',
   FEE_STD                 char(256),  comment '收费标准',
   FEE_DESC                 longtext(40000),  comment '收费依据',
   CREATE_USER          char(50),      comment '创建人', 
   CREATE_TIME          timestamp,     comment '创建时间',
   UPDATE_USER          char(50),      comment '最后更新人',
   UPDATE_TIME          timestamp      comment '最后更新时间',
);

alter table GOV_SERVIES_FEE comment '服务业务收费';

alter table GOV_DEPT_DUTY_REL add constraint FK_Relationship_2 foreign key ()
      references GOV_DEPT_LIST on delete restrict on update restrict;

alter table GOV_DEPT_DUTY_REL add constraint FK_Relationship_6 foreign key ()
      references GOV_DUTY_LIST on delete restrict on update restrict;

alter table GOV_DEPT_ITEM_REL add constraint FK_Relationship_1 foreign key ()
      references GOV_DEPT_LIST on delete restrict on update restrict;

alter table GOV_DEPT_ITEM_REL add constraint FK_Relationship_5 foreign key ()
      references GOV_ITEM_LIST on delete restrict on update restrict;

alter table GOV_DUTY_LIST add constraint FK_Relationship_4 foreign key ()
      references GOV_ITEMS_TYPE_DEF on delete restrict on update restrict;

alter table GOV_ITEM_LIST add constraint FK_Relationship_3 foreign key ()
      references GOV_ITEMS_TYPE_DEF on delete restrict on update restrict;

alter table GOV_QUERY_ANSWER add constraint FK_Relationship_11 foreign key ()
      references GOV_SERVICES_LIST on delete restrict on update restrict;

alter table GOV_SERVICES_FLOW add constraint FK_Relationship_10 foreign key ()
      references GOV_SERVICES_LIST on delete restrict on update restrict;

alter table GOV_SERVICES_LIST add constraint FK_Relationship_8 foreign key ()
      references GOV_ITEM_LIST on delete restrict on update restrict;

alter table GOV_SERVICES_MATERIAL add constraint FK_Relationship_9 foreign key ()
      references GOV_SERVICES_LIST on delete restrict on update restrict;

alter table GOV_SERVIES_FEE add constraint FK_Relationship_12 foreign key ()
      references GOV_SERVICES_LIST on delete restrict on update restrict;

