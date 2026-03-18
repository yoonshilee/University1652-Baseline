# Challenge Report, Cross-view Ground-to-Satellite Geo-localization (Optional)

## Assessment Rule

Challenge (Optional): 10% (at least 2 pages using provided latex template) before 15 April

## Submission Info

The submission website is at <https://codalab.lisn.upsaclay.fr/competitions/22073>. After you get result, please also submit a short report on UMmoodle.

## Task Introduction

This year’s focus is specifically on matching partial street images to corresponding satellite images (illustrated in Figure 3 of the proposal). By concentrating on partial views, our aim is to more accurately reflect real-world scenarios where obstructions or limited sensor angles may restrict the field of view, such as during low-altitude UAV operations for navigation, search-and-rescue missions, and autonomous flight. We harness University-1652 as the challenge dataset, which provides 2,579 street images as query and 951 gallery satellite images. To encourage broader participation and innovation, we will make University-1652 training set available through our website with name-masked test set, along with a public leaderboard.

## Related Resources

- Check challenge details at Section 5 in <https://www.zdzheng.xyz/files/MM25_Workshop_Proposal_Drone.pdf> ([MM25_Workshop_Proposal_Drone.pdf](MM25_Workshop_Proposal_Drone.pdf))
- The training dataset can be download by sending the request <https://github.com/layumi/University1652-Baseline/blob/master/Request.md>. Usually I will reply the download link in 5 minutes.
- The test query can be downloaded at (Please check the challenge website).
- The submission example can be found at Baseline Submission <https://github.com/spyflying/ACMMM2025Workshop-UAV/blob/main/answer.zip> ([answer.txt](answer.txt)).

## Submission Requirements

1. Please zip it as “answer.zip” to submit the result, and it is crucial to name the file exactly as answer.txt within the zip, as otherwise the evaluation will fail.
2. Please return the top-10 satellite names. For example, the first query is “VdthudbGjJ4aaNkl.jpeg”. Therefore, the first line of returned result in “answer.txt” should be the format as follows from Rank-1 to Rank-10:

    ```plaintext
    ptHYAN3piG3YwOft I9bzP8jnLlz9zpMi c3vVTLCzTAVzuapU gkriPL4PNtcWoHgg iIL2ASdQ5vrFsJs0 TinwNxUGYAzz0kTO XilyyHqywhUBxHfT WLasj720MnF13zPI Qz4NypYGPhHdiAvn gO2hUfIHC8N4ZWKz
    ```

3. Please return the result following the order of query at Query Name Txt <https://github.com/spyflying/ACMMM2025Workshop-UAV/blob/main/query_street_name.txt> ([query_street_name.txt](query_street_name.txt)). It will be 2759 lines.

## Contact

If you meet any difficulties, please contact TAs and me.

## Related Schedule

(15/04: Challenge DDL)
