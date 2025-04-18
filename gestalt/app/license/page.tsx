import "@/styles/License.css"


export default function LicensePage() {
    return (
      <div className="license-body">
        <div className="license-container">
          <h1 className="license-title">Academic Software License</h1>
  
          <p className="license-highlight">
            © 2024 University of California, Riverside (“Institution”).
          </p>
  
          <p className="license-text">
            Academic or nonprofit researchers are permitted to use this Software (as defined below) subject to Paragraphs 1–4:
          </p>
  
          <div className="license-paragraph">
            <p>
              <strong>1.</strong> Institution hereby grants to you free of charge, so long as you are an academic or
              nonprofit researcher, a nonexclusive license under Institution’s copyright ownership interest in this
              software and any derivative works made by you thereof (collectively, the “Software”) to use, copy, and make
              derivative works of the Software solely for educational or academic research purposes, in all cases subject
              to the terms of this Academic Software License. Except as granted herein, all rights are reserved by
              Institution, including the right to pursue patent protection of the Software.
            </p>
          </div>
  
          <div className="license-paragraph">
            <p>
              <strong>2.</strong> Please note you are prohibited from further transferring the Software -- including any
              derivatives you make thereof -- to any person or entity. Failure by you to adhere to the requirements in
              Paragraphs 1 and 2 will result in immediate termination of the license granted to you pursuant to this
              Academic Software License effective as of the date you first used the Software.
            </p>
          </div>
  
          <div className="license-paragraph">
            <p>
              <strong>3.</strong> IN NO EVENT SHALL INSTITUTION BE LIABLE TO ANY ENTITY OR PERSON FOR DIRECT, INDIRECT,
              SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS
              SOFTWARE, EVEN IF INSTITUTION HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. INSTITUTION SPECIFICALLY
              DISCLAIMS ANY AND ALL WARRANTIES, EXPRESS AND IMPLIED, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED WARRANTIES
              OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE IS PROVIDED “AS IS.” INSTITUTION HAS
              NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS OF THIS SOFTWARE.
            </p>
          </div>
  
          <div className="license-paragraph">
            <p>
              <strong>4.</strong> Any academic or scholarly publication arising from the use of this Software or any
              derivative works thereof will include the following acknowledgment: The Software used in this research was
              created by Sundararajan Venkatadriagaram of UC Riverside. © 2024 UCR [Sundararajan Venkatadriagaram].
            </p>
          </div>
  
          <p className="license-highlight">
            Commercial entities: please contact{" "}
            <a href="mailto:otc@ucr.edu" className="footer-link">
              otc@ucr.edu
            </a>{" "}
            for licensing opportunities.
          </p>
        </div>
      </div>
    );
  }
  


