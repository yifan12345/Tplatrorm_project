//清理下拉选项
function clearOption(cmb) {
    for (let i = 0; i <= cmb.length; i++) {
        cmb.options.remove(cmb[i]);
    }
}

//创建下拉选项
function cmbAddOption(cmb, obj) {
    let option = document.createElement("option");
    cmb.options.add(option);
    option.innerHTML = obj.name;
    option.value = obj.id;
}

// 获取项目列表
var ProjectInit = function (_cmbProject) {
    var cmbProject = document.getElementById(_cmbProject);


    function getProjectListInfo() {
        $.get("/project/get_project_list/", {}, function (resp) {
            if (resp.status === 10200) {
                console.log(resp.data);
                let dataList = resp.data;
                for (let i = 0; i < dataList.length; i++) {
                    cmbAddOption(cmbProject, dataList[i]);
                }
            } else {
                window.alert(resp.message);
            }
        });
    }

    // 调用getCaseListInfo函数
    getProjectListInfo();
};

// 获取某一个项目的模块列表
var ModuleInit = function (_cmbModule, pid) {
    var cmbModule = document.getElementById(_cmbModule);

    function getModuleListInfo() {
        $.post("/module/get_module_list/", {
            "pid": pid
        }, function (resp) {
            if (resp.status === 10200) {
                console.log(resp.data);
                let dataList = resp.data;
                clearOption(cmbModule);
                for (let i = 0; i < dataList.length; i++) {
                    cmbAddOption(cmbModule, dataList[i]);
                }
                $("#module_name").selectpicker("refresh");
            } else {
                window.alert(resp.message);
            }
        });
    }

    // 调用getCaseListInfo函数
    getModuleListInfo();

};


//获取用例信息
var TestCaseInit = function () {
    var url = document.location;
    var cid = url.pathname.split("/")[3];
    $.post("/case_list/get_case_info/",
        {
            cid: cid,
        },
        function (resp) {
            console.log("返回结果：", resp);
            //URL
            document.querySelector("#in_url").value = resp.data.url;
            //请求方法
            if (resp.data.method === 1) {
                document.querySelector("#get").setAttribute("checked", "");
            } else if (resp.data.method === 2) {
                document.querySelector("#post").setAttribute("checked", "");
            } else if (resp.data.method === 3) {
                document.querySelector("#put").setAttribute("checked", "");
            } else if (resp.data.method === 4) {
                document.querySelector("#delete").setAttribute("checked", "");
            }
            //请求头
            document.querySelector("#header").value = resp.data.header;
            //参数类型
            if (resp.data.par_type === 1) {
                document.querySelector("#form").setAttribute("checked", "");
            } else if (resp.data.par_type === 2) {
                document.querySelector("#json").setAttribute("checked", "");
            }
            //请求参数
            document.querySelector("#parameter").value = resp.data.par_body;
            //断言类型
            if (resp.data.assert_type === 1) {
                document.querySelector("#Contains").setAttribute("checked", "");
            } else if (resp.data.assert_type === 2) {
                document.querySelector("#Mathches").setAttribute("checked", "");
            }
            //断言的数据
            document.querySelector("#assert_text").value = resp.data.assert_text;

            //用例名称
            document.querySelector("#case_name").value = resp.data.case_name;

            //所属模块

        }
    )
};
