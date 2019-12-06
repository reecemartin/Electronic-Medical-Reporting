const form = {
  "sections": [
      {
          "title": "#This template describes a Common Data Element for CT Stroke by the American College of Radiologists",
          "subsections": [],
          "questions": [
              {
                  "title": "",
                  "question_id": "76234.100004300",
                  "question_type": "MC",
                  "state": true,
                  "dependents": {},
                  "options": "@Adrenocortical neoplasm@"
              }
          ],
          "section_id": "76242.100004300"
      },
      {
          "title": "Administrative & Identification Data",
          "subsections": [],
          "questions": [
              {
                  "title": "Report Date",
                  "question_id": "76219.100004300",
                  "dependents": {},
                  "question_type": "ST",
                  "state": true
              }
          ],
          "section_id": "76221.100004300"
      },
      {
          "title": "Findings",
          "subsections": [],
          "questions": [
              {
                  "title": "Hyperacute signs",
                  "question_id": "77913.100004300",
                  "question_type": "MC",
                  "state": true,
                  "dependents": {},
                  "options": "Yes|No"
              }
          ],
          "section_id": "77659.100004300"
      }
  ],
  "free_questions": [
      {
          "title": "Comment(s)",
          "question_id": "76386.100004300",
          "question_type": "ST",
          "state": true
      }
  ],
  "form": {
      "form_id": "CT_Stroke_CCO.358_1.0.0.DRAFT_sdcFDF",
      "form_title": "CCO Synoptic Template for  Stroke",
      "package_id": "PKG_ACR_CT_STROKE",
      "form_footer": "(c) 2018 College of American Pathologists.  All rights reserved.  License required for use."
  }
}


export default form;
