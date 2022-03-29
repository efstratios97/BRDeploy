import { ref } from "vue";

export default async function useGetDatasetOptionsCascaded(axios) {
    const result = ref("")

    const fetchPost = async () => {
        const res = await axios.get("/get_datasets_only_name/" + localStorage.loggedUser)
            .then((res) => {
                var datasets_tmp = [];
                var datasets_tmp_plain_list = [];
                const label_prefix = "Dataset Category: ";
                for (let index = 0; index < res.data.data.length; index++) {
                    if (
                        datasets_tmp_plain_list.indexOf(
                            label_prefix + res.data.data[index]["label"]
                        ) < 0
                    ) {
                        datasets_tmp.push({
                            label: label_prefix + res.data.data[index]["label"],
                            dataset: [],
                        });
                        datasets_tmp_plain_list.push(
                            label_prefix + res.data.data[index]["label"]
                        );
                    }
                }
                for (let index = 0; index < res.data.data.length; index++) {
                    var index_dataset_tmp = datasets_tmp_plain_list.indexOf(
                        label_prefix + res.data.data[index]["label"]
                    );
                    if (index === 0) {
                        datasets_tmp[index_dataset_tmp]["dataset"].push({
                            dataset_desc:
                                "Dataset: " +
                                res.data.data[index]["name"] +
                                "   |   " +
                                "NEWEST: " +
                                res.data.data[index]["creation_date"].split(",")[1] +
                                "   |   " +
                                "ID: " +
                                res.data.data[index]["dataset_id"],
                        });
                        var label_desc = res.data.data[index]["label"];
                    } else {
                        datasets_tmp[index_dataset_tmp]["dataset"].push({
                            dataset_desc:
                                "Dataset: " +
                                res.data.data[index]["name"] +
                                "   |   " +
                                "Created: " +
                                res.data.data[index]["creation_date"].split(",")[1] +
                                "   |   " +
                                "ID: " +
                                res.data.data[index]["dataset_id"],
                        });
                        label_desc = res.data.data[index]["label"];
                    }
                }
                var datasets = datasets_tmp
                result.value = datasets
                // resolve({ datasets, label_desc })
            });
        // })
    }
    await getDatasetsOptionsCascaded()
    return { result }
}